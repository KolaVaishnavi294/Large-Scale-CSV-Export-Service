from dataclasses import dataclass
from datetime import datetime

@dataclass
class ExportJob:
    id: str
    status: str
    total_rows: int = 0
    processed_rows: int = 0
    created_at: datetime = datetime.utcnow()
    completed_at: datetime = None
    error: str = None