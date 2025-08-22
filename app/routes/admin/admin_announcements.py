# app/routes/admin/announcements.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from app.models.announcement_model import Announcement
from app.models.member_model import Member
from app.schemas.announcement_schema import (
    AnnouncementCreate, 
    AnnouncementUpdate, 
    AnnouncementResponse
)
from app.dependencies import require_admin

router = APIRouter()


@router.post("", response_model=AnnouncementResponse)
async def create_announcement(
    announcement: AnnouncementCreate,
    current_user: Member = Depends(require_admin)
):
    """Create a new announcement (Admin only)"""
    db_announcement = Announcement(
        **announcement.dict(),
        author=str(current_user.id)
    )
    await db_announcement.create()
    
    # Convert to response model with string ID
    announcement_dict = db_announcement.dict(exclude={"id"})
    return AnnouncementResponse(
        **announcement_dict,
        id=str(db_announcement.id)
    )

@router.get("", response_model=List[AnnouncementResponse])
async def get_announcements(
    current_user: Member = Depends(require_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    published_only: bool = Query(False)
):
    """Get all announcements (Admin only)"""
    query = {}
    if published_only:
        query["is_published"] = True
    
    announcements = await Announcement.find(
        query
    ).sort("-created_at").skip(skip).limit(limit).to_list()
    
    # Convert to response models with string IDs
    return [
        AnnouncementResponse(
            **announcement.dict(exclude={"id"}),
            id=str(announcement.id)
        )
        for announcement in announcements
    ]

@router.get("/{id}", response_model=AnnouncementResponse)
async def get_announcement(
    id: str,
    current_user: Member = Depends(require_admin)
):
    """Get a specific announcement (Admin only)"""
    announcement = await Announcement.get(id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    # Convert to response model with string ID
    announcement_dict = announcement.dict(exclude={"id"})
    return AnnouncementResponse(
        **announcement_dict,
        id=str(announcement.id)
    )

@router.put("/{id}", response_model=AnnouncementResponse)
async def update_announcement(
    id: str,
    announcement: AnnouncementUpdate,
    current_user: Member = Depends(require_admin)
):
    """Update an announcement (Admin only)"""
    db_announcement = await Announcement.get(id)
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    update_data = announcement.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await db_announcement.update({"$set": update_data})
    
    # Get the updated announcement
    updated_announcement = await Announcement.get(id)
    
    # Convert to response model with string ID
    announcement_dict = updated_announcement.dict(exclude={"id"})
    return AnnouncementResponse(
        **announcement_dict,
        id=str(updated_announcement.id)
    )



@router.delete("/{id}")
async def delete_announcement(
    id: str,
    current_user: Member = Depends(require_admin)
):
    """Delete an announcement (Admin only)"""
    announcement = await Announcement.get(id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    await announcement.delete()
    return {"message": "Announcement deleted successfully"}