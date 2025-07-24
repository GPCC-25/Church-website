from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.announcement_models import Announcement, UpdateAnnouncement
from bson import ObjectId
from datetime import datetime


collection_name = "announcements"

# create announcement
async def create_announcement(db: AsyncIOMotorDatabase, data: Announcement):
    announcement = data.dict()
    result = await db[collection_name].insert_one(announcement)
    return {"id": str(result.inserted_id), **announcement}


#get all announcement
async def get_announcements(db:AsyncIOMotorDatabase):
    announcements = []
    async for ann in db[collection_name].find():
        ann["_id"] = str(ann["_id"])
        announcements.append(ann)
    return announcements


#update announcement
async def update_announcement(db: AsyncIOMotorDatabase, announcement_id: str,
                               data: UpdateAnnouncement):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        result = await db[collection_name].update_one(
            {"_id": ObjectId(announcement_id)}, {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Announcement not found")
        return {"msg": "Announcemnet updated"}
    raise HTTPException(status_code=400, details="No fields to update")

