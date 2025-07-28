from fastapi import Depends, HTTPException, status
from app.routes.auth import get_current_user
from app.models.member_model import Member


def require_admin(current_user: Member = Depends(get_current_user)):
    if current_user.role not in ["Admin", "Staff"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )
    return current_user
    