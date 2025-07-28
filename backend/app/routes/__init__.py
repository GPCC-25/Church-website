from fastapi import APIRouter
from . import auth, members, events
from .admin import admin_router

main_router = APIRouter()

main_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
main_router.include_router(members.router, prefix="/members", tags=["Member Profile"])
main_router.include_router(events.router, prefix="/events", tags=["Events"])
main_router.include_router(admin_router, prefix="/admin", tags=["Admin"])