from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Announcement(BaseModel):
    title: str
    content: str
    author: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class UpdateAnnouncement(BaseModel):
    title: Optional[str]
    content: Optional[str]