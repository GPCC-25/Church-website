from beanie import Document
from datetime import datetime
from pydantic import Field
from typing import Optional


class AttendanceCheckIn(Document):
    member_id: str
    event_id: str
    check_in_time: datetime = Field(default_factory=datetime.utcnow)
    role: str
    age_group: Optional[str] = None

    class Settings:
        name = "attendance_records"