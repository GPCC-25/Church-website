from fastapi import APIRouter, Depends
from app.controllers.announcement_controller import (create_announcement, 
                                                     get_announcements,
                                                     update_announcement)
from app.models.announcement_models import Announcement, UpdateAnnouncement
from app.database.database import get_database


router = APIRouter(prefix="/announcements", tags=["Announcements"])

@router.post("/")
async def create_announcement(data: Announcement, db=Depends(get_database)):
    return await create_announcement(db, data)

@router.get("/")
async def list_announcements(db=Depends(get_database)):
    return await get_announcements(db)


@router.put("/{announcement_id}")
async def update_announcement(announcement_id: str, 
                              data: UpdateAnnouncement,
                                db=Depends(get_database)):
    return await update_announcement(db, announcement_id, data)

