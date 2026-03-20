import asyncio
import os
import gzip
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import StreamingResponse, FileResponse

from .exporter import stream_export
from .job_manager import create_job, get_job, cancel_job, tasks
from .database import get_pool
from app.config import settings

router = APIRouter()


@router.post("/exports/csv")
async def create_export(
    columns: str = None,
    delimiter: str = ",",
    quoteChar: str = '"'
):

    job = create_job()

    filepath = f"{settings.EXPORT_STORAGE_PATH}/{job.id}.csv"

    if columns:
        columns = columns.split(",")
    else:
        columns = [
            "id","name","email","signup_date",
            "country_code","subscription_tier","lifetime_value"
        ]

    pool = await get_pool()

    task = asyncio.create_task(
        stream_export(
            pool,
            job,
            filepath,
            filters={},
            columns=columns,
            delimiter=delimiter,
            quotechar=quoteChar
        )
    )

    tasks[job.id] = task

    return {
        "exportId": job.id,
        "status": "pending"
    }


@router.get("/exports/{exportId}/status")
async def export_status(exportId: str):

    job = get_job(exportId)

    if not job:
        raise HTTPException(404)

    percent = 0
    if job.total_rows:
        percent = round((job.processed_rows/job.total_rows)*100,2)

    return {
        "exportId": job.id,
        "status": job.status,
        "progress": {
            "totalRows": job.total_rows,
            "processedRows": job.processed_rows,
            "percentage": percent
        },
        "error": job.error,
        "createdAt": job.created_at,
        "completedAt": job.completed_at
    }


@router.delete("/exports/{exportId}")
async def cancel_export(exportId: str):

    cancel_job(exportId)

    path = f"{settings.EXPORT_STORAGE_PATH}/{exportId}.csv"

    if os.path.exists(path):
        os.remove(path)

    return Response(status_code=204)


@router.get("/exports/{exportId}/download")
async def download(exportId: str, request: Request):

    filepath = f"{settings.EXPORT_STORAGE_PATH}/{exportId}.csv"

    if not os.path.exists(filepath):
        raise HTTPException(404)

    if "gzip" in request.headers.get("Accept-Encoding",""):

        def iterfile():
            with open(filepath,"rb") as f:
                with gzip.GzipFile(fileobj=None, mode="wb") as gz:
                    yield gz.write(f.read())

        return StreamingResponse(
            iterfile(),
            media_type="application/gzip",
            headers={"Content-Encoding":"gzip"}
        )

    return FileResponse(
        filepath,
        media_type="text/csv",
        filename=f"export_{exportId}.csv",
        headers={"Accept-Ranges":"bytes"}
    )