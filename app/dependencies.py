from fastapi import Depends, HTTPException, status
from app.utils.auth import get_current_active_user, get_current_user
from app.models.member_model import Member

__all__ = ["get_current_user", "get_current_active_user", "require_admin"]

def require_admin(current_user: Member = Depends(get_current_user)):
    if current_user.role not in ["Admin", "Staff"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )
    return current_user