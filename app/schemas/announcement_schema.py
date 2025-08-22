# app/schemas/announcement_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.announcement_model import AnnouncementPriority, AnnouncementTarget

class AnnouncementBase(BaseModel):
    title: str
    content: str
    priority: AnnouncementPriority = AnnouncementPriority.NORMAL
    target: AnnouncementTarget = AnnouncementTarget.ALL
    target_departments: List[str] = Field(default_factory=list)
    expires_at: Optional[datetime] = None

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[AnnouncementPriority] = None
    target: Optional[AnnouncementTarget] = None
    target_departments: Optional[List[str]] = None
    is_published: Optional[bool] = None
    expires_at: Optional[datetime] = None

class AnnouncementResponse(AnnouncementBase):
    id: str
    author: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True



        