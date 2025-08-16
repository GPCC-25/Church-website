from fastapi import APIRouter, Depends, HTTPException
from app.models.member_model import Member
from app.schemas.member_schema import MemberOut, MemberSelfUpdate
from app.dependencies import get_current_user, get_current_active_user
import logging


logger = logging.getLogger(__name__)
router = APIRouter(tags=["Member Profile"])

def convert_member_to_out(member: Member) -> dict:
    return {
        "id": str(member.id),
        "first_name": member.first_name,
        "last_name": member.last_name,
        "email": member.email,
        "phone": member.phone,
        "role": member.role,
        "join_date": member.join_date,
        "is_active": member.is_active,
        "departments": member.departments
    }


@router.get("/me", response_model=MemberOut)
async def update_my_profile(
    update_data: MemberSelfUpdate,
    current_user: Member = Depends(get_current_user)):
    try:
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(current_user, field, value)

        await current_user.save()

        return convert_member_to_out(current_user)
    
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(
            status_code = 500,
            detail="Failed to update profile"
        )


@router.put("/me", response_model=MemberOut)
async def get_my_profile(
    current_user: Member = Depends(get_current_user)
):
    
    try:
        return convert_member_to_out(current_user)
    except Exception as e:
        logger.error(f"Error fetching current user: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch user data"
        )