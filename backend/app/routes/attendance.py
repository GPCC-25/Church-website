from app.models.attendance_model import AttendanceCheckIn
from app.schemas.attendance_schema import CheckInCreate, CheckInOut
from app.utils.auth import get_current_user
from app.models.member_model import Member
from fastapi import APIRouter, Depends, HTTPException
from app.models.settings_model import AttendanceSettings


router = APIRouter(tags=["Attendance"])


@router.get("/form-url", response_model=dict)
async def get_attendance_form_url(current_user: Member = Depends(get_current_user)):
    settings = await AttendanceSettings.find_one()
    if not settings or not settings.google_form_url:
        raise HTTPException(
            status_code=404,
            detail = "No attendance form configured"
        )
    return {"url": settings.google_form_url}


"""@router.post("/check-in", response_model=CheckInOut)
async def check_in_to_service(
    check_in_data: CheckInCreate,
    current_user: Member = Depends(get_current_user)
):
    new_checkin = AttendanceCheckIn(
        member_id=str(current_user.id), **check_in_data.dict())
    await new_checkin.insert()
    return new_checkin
"""