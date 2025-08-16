from fastapi import APIRouter, Depends, HTTPException, status
from app.models.prayer_testimony_model import PrayerRequest, Testimony, Comment
from app.schemas.prayer_testimony_schema import (PrayerRequestCreate,
                                                 PrayerRequestOut,
                                                 PrayerCounterUpdate,
                                                 CommentBase,
                                                 TestimonyOut,
                                                 TestimonyCreate)
from app.models.member_model import Member
from app.utils.auth import get_current_user
from beanie import PydanticObjectId
from typing import List
import logging


logger = logging.getLogger(__name__)
router = APIRouter(tags=["Prayer & Testimony"])


@router.post("/prayer-requests", response_model=PrayerRequestOut)
async def submit_prayer_request(
    request_data: PrayerRequestCreate,
    current_user: Member = Depends(get_current_user)
):
    new_request = PrayerRequest(
        member_id=str(current_user.id),
        **request_data.dict()
    )

    await new_request.insert()
    return PrayerRequestOut.model_validate(new_request)



@router.get("/prayer-requests", response_model=List[PrayerRequestOut])
async def get_public_prayer_requests():
    requests = await PrayerRequest.find(
        PrayerRequest.is_public == True,
        PrayerRequest.is_approved == True
    ).to_list()
    return requests



@router.post("/prayer-requests/{request_id}/pray")
async def increment_prayer_count(
    request_id: PydanticObjectId,
    update: PrayerCounterUpdate,
    current_user: Member = Depends(get_current_user)
):
    request = await PrayerRequest.get(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Prayer request not found")
    request.prayer_count += update.increment
    await request.save()

    return {"message": "Prayer count updated"}



@router.post("/prayer-requests/{request_id}/comments")
async def add_prayer_comment(
    request_id: PydanticObjectId,
    comment_data: CommentBase,
    current_user: Member = Depends(get_current_user)
):
    request = await PrayerRequest.get(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Prayer request not found")
    
    new_comment = Comment(
        member_id=str(current_user.id),
        text=comment_data.text
    )
    request.comments.append(new_comment)
    await request.save()
    return {"message": "Comment added"}



@router.post("/testimonies", response_model=TestimonyOut)
async def submit_testimony(
    testimony_data: TestimonyCreate,
    current_user: Member = Depends(get_current_user)
):
    new_testimony = Testimony(
        member_id=str(current_user.id),
        **testimony_data.dict()
    )
    await new_testimony.insert()
    return TestimonyOut.model_validate(new_testimony)




@router.get("/testimonies", response_model=List[TestimonyOut])
async def get_public_testimonies():
    testimonies = await Testimony.find(
        Testimony.is_approved == True
    ).to_list()
    return testimonies


@router.post("testimonies/{testimony_id}/comments")
async def add_testimony_comment(
    testimony_id: PydanticObjectId,
    comment_data: CommentBase,
    current_user: Member = Depends(get_current_user)
):
    testimony = await Testimony.get(testimony_id)
    if not testimony:
        raise HTTPException(status_code=404, detail="Testimony not found")
    

    new_comment = Comment(
        member_id=str(current_user.id),
        text=comment_data.text
    )

    testimony.comments.append(new_comment)
    await testimony.save()
    return {"message": "Comment added"}