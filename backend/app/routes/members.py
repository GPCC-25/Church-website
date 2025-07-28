from fastapi import APIRouter, Depends
from app.models.member_model import Member
from app.schemas.member_schema import MemberOut, MemberSelfUpdate
from app.routes.auth import get_current_user

router = APIRouter(tags=["Member Profile"])

@router.get("/me", response_model=MemberOut)
async def get_my_profile(current_user: Member = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=MemberOut)
async def update_my_profile(
    update_data: MemberSelfUpdate,
    current_user: Member = Depends(get_current_user)
):
    
    update_dict = update_data.dict(exclude_unset=True)
    
    
    await current_user.set(update_dict)
    
    
    return await Member.get(current_user.id)