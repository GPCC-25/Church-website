from fastapi import APIRouter, HTTPException
from app.models.member_model import Member, VALID_ROLES
from beanie import PydanticObjectId
from pydantic import BaseModel

router = APIRouter()

class PromoteUserRequest(BaseModel):
    new_role: str  # "Admin" or "Staff"

@router.post("/promote/{user_id}")
async def promote_user(user_id: PydanticObjectId, request: PromoteUserRequest):
    if request.new_role not in VALID_ROLES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Must be one of: {', '.join(VALID_ROLES)}"
        )
    
    user = await Member.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = request.new_role
    await user.save()
    return {"message": f"User promoted to {request.new_role}"}