from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class AnnouncementPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class AnnouncementTarget(str, Enum):
    ALL = "all"
    MEMBERS = "members"
    STAFF = "staff"
    DEPARTMENTS = "departments"

class Announcement(Document):
    title: str
    content: str
    author: str  # Admin who created the announcement
    priority: AnnouncementPriority = AnnouncementPriority.NORMAL
    target: AnnouncementTarget = AnnouncementTarget.ALL
    target_departments: List[str] = Field(default_factory=list)  # If target is DEPARTMENTS
    is_published: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    
    class Settings:
        name = "announcements"
        indexes = [
            [("is_published", 1), ("expires_at", 1), ("created_at", -1)],
            [("target", 1), ("target_departments", 1)],
        ]