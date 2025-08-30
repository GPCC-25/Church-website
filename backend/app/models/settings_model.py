from beanie import Document
from pydantic import BaseModel, Field


class AttendanceSettings(Document):
    google_form_url: str = Field(default="", description="Google form URL for attendance")

    class Settings:
        name = "attendance_settings"


        