import uuid
from datetime import datetime

jobs = {}
tasks = {}

class Job:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.status = "pending"
        self.total_rows = 0
        self.processed_rows = 0
        self.error = None
        self.created_at = datetime.utcnow().isoformat()
        self.completed_at = None


def create_job():
    job = Job()
    jobs[job.id] = job
    return job


def get_job(job_id):
    return jobs.get(job_id)


def cancel_job(job_id):
    if job_id in tasks:
        tasks[job_id].cancel()
        del tasks[job_id]

    if job_id in jobs:
        jobs[job_id].status = "cancelled"