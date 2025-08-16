from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CheckInCreate(BaseModel):
    event_id: str
    role: str
    age_group: Optional[str] = None


class CheckInOut(CheckInCreate):
    id: str
    member_id: str
    check_in_time: datetime

    model_config = ConfigDict(from_attributes=True)


class AttendanceReportRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    role: Optional[str] = None
    age_group: Optional[str] = None
