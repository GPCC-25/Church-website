from fastapi import APIRouter
from app.controllers import auth_controllers
from app.schemas.user_schema import UserCreate, UserLogin


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register(user: UserCreate):
    return await auth_controllers.register_user(user)

@router.post("/login")
async def login(user: UserLogin):
    return await auth_controllers.login_user(user)