from fastapi import APIRouter, Depends, HTTPException
from app.models.settings_model import AttendanceSettings
from app.schemas.setting_schema import AttendanceSettingsSchema, AttendanceSettingsResponse
from app.dependencies import require_admin
from beanie import PydanticObjectId
import logging



router = APIRouter(tags=["Admin - Attendance Settings"])
logger = logging.getLogger(__name__)



@router.put("/attendance/form_url", response_model=AttendanceSettingsResponse)
async def set_attendance_form_url(settings_data: AttendanceSettingsSchema,
                                  current_user = Depends(require_admin)):
    settings = await AttendanceSettings.find_one()

    if not settings:
        settings = AttendanceSettings(
                                      google_form_url=settings_data.google_form_url)
        await settings.insert()
    else:
        settings.google_form_url = settings_data.google_form_url
        await settings.save()
    return {"google_form_url": settings.google_form_url}



@router.get("/attendance/form_url", response_model=AttendanceSettingsResponse)
async def get_attendance_form_url(current=Depends(require_admin),
                                  ):
    settings = await AttendanceSettings.find_one()
    if not settings or not settings.google_form_url:
        return {"google_form_url": ""}
    return {"google_form_url": settings.google_form_url}