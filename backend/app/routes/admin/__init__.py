from fastapi import APIRouter, Depends
from app.dependencies import require_admin
from . import members, events, users, roles


admin_router = APIRouter(
    dependencies=[Depends(require_admin)]
)

admin_router.include_router(members.router, prefix="/members", tags=["Admin - Members"])
admin_router.include_router(events.router, prefix="/events", tags=["Admin - Events"])
admin_router.include_router(users.router, prefix="/users", tags=["Admin - Users"])
admin_router.include_router(roles.router, prefix="/roles", tags=["Admin - Roles"])