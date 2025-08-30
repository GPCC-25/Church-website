from fastapi import APIRouter, Depends
from app.dependencies import require_admin
from . import admin_announcements, members, events, users, roles, attendance_settings, prayer_testimony_admin


admin_router = APIRouter(
    dependencies=[Depends(require_admin)]
)

admin_router.include_router(members.router, prefix="/members", tags=["Admin - Members"])
admin_router.include_router(events.router, prefix="/events", tags=["Admin - Events"])
admin_router.include_router(users.router, prefix="/users", tags=["Admin - Users"])
admin_router.include_router(roles.router, prefix="/roles", tags=["Admin - Roles"])
admin_router.include_router(prayer_testimony_admin.router, prefix="/admin-prayer&testimony", tags=["Admin - Prayer & Testimony"])
admin_router.include_router(attendance_settings.router, prefix="/admin", tags=["Admin - Attendance Settings"])
admin_router.include_router(admin_announcements.router, prefix="/admin/announcements", tags=["Admin - Announcements"])
