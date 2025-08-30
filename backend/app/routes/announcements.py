# app/routes/member/announcements.py
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from datetime import datetime

from app.models.announcement_model import Announcement
from app.models.member_model import Member
from app.schemas.announcement_schema import AnnouncementResponse
from app.dependencies import get_current_user

router = APIRouter()

@router.get("", response_model=List[AnnouncementResponse])
async def get_announcements(
    current_user: Member = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    priority: Optional[str] = Query(None)
):
    """Get published announcements relevant to the current user"""
    # Base query for published, non-expired announcements
    query = {
        "is_published": True,
        "$or": [
            {"expires_at": {"$gt": datetime.utcnow()}},
            {"expires_at": None}
        ]
    }
    
    # Filter by priority if specified
    if priority:
        query["priority"] = priority
    
    # Check if user is staff (admin, pastor, elder)
    is_staff = current_user.role in ["Admin", "Staff"]
    
    # Filter by target audience
    target_query = {
        "$or": [
            {"target": "all"},
            {"target": "members"},
            {"target": "staff", "$expr": {"$eq": [is_staff, True]}},
            {"target": "departments", "target_departments": {"$in": current_user.departments}}
        ]
    }
    
    # Combine queries
    final_query = {"$and": [query, target_query]}
    
    announcements = await Announcement.find(
        final_query
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
    current_user: Member = Depends(get_current_user)
):
    """Get a specific announcement"""
    try:
        announcement = await Announcement.get(id)
    except:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    if not announcement or not announcement.is_published:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    # Check if announcement is expired
    if announcement.expires_at and announcement.expires_at < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Announcement has expired")
    
    # Check if user has access to this announcement
    is_staff = current_user.role in ["Admin", "Staff"]
    has_access = (
        announcement.target == "all" or
        announcement.target == "members" or
        (announcement.target == "staff" and is_staff) or
        (announcement.target == "departments" and 
         any(dept in announcement.target_departments for dept in current_user.departments))
    )
    
    if not has_access:
        raise HTTPException(status_code=403, detail="Not authorized to view this announcement")
    
    # Convert to response model with string ID
    announcement_dict = announcement.dict(exclude={"id"})
    return AnnouncementResponse(
        **announcement_dict,
        id=str(announcement.id)
    )