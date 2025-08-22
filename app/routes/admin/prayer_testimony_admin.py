from fastapi import APIRouter, HTTPException, Depends
from beanie import PydanticObjectId
from app.models.prayer_testimony_model import PrayerRequest, Testimony
from app.schemas.prayer_testimony_schema import PrayerRequestOut, TestimonyOut
from app.dependencies import require_admin
from typing import List
import logging


logger = logging.getLogger(__name__)
router = APIRouter(tags=["Admin - Prayer & Testimony"])



@router.get("/prayer-requests", response_model=List[PrayerRequestOut])
async def get_all_prayer_requests(current_user = Depends(require_admin)):
    return await PrayerRequest.find_all().to_list()



@router.put("/prayer-requests/{request_id}/approve")
async def approve_prayer_request(
    request_id: PydanticObjectId,
    current_user = Depends(require_admin)
):
    request = await PrayerRequest.get(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Prayer request not found")
    
    request.is_approved = True
    await request.save()
    return {"message": "Prayer request approved"}



@router.put("/testimonies/{testimony_id}/moderate")
async def moderate_testimony(
    testimony_id: PydanticObjectId,
    action: str, # "approve", "reject", "edit"
    content: str = None,
    current_user = Depends(require_admin)
):
    testimony = await Testimony.get(testimony_id)
    if not testimony:
        raise HTTPException(status_code=404, detail="Testimony not found")
    
    if action == "approve":
        testimony.is_approved = True
    elif action == "reject":
        testimony.is_approved = False
    elif action == "edit" and content:
        testimony.content = content

    await testimony.save()
    return {"message": f"Testimony {action} succesful"}
