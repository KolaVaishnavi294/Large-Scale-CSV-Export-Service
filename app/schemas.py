from pydantic import BaseModel


class ExportResponse(BaseModel):
    exportId: str
    status: str