from beanie import Document
from datetime import datetime
from pydantic import Field, BaseModel
from typing import List, Optional



class Comment(BaseModel):
    member_id: str
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PrayerRequest(Document):
    member_id: str
    content: str
    is_public: bool = True
    is_approved: bool = False
    prayer_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    comments: List[Comment] = []

    class Settings:
        name = "prayer_requests"


class Testimony(Document):
    member_id: str
    content: str
    is_approved: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    comments: List[Comment] = []

    class Settings:
        name = "testimonies"