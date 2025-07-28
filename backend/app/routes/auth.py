from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.member_model import Member
from app.schemas.auth_schema import TokenResponse, UserRegister, PasswordUpdate
from app.utils.auth import (create_access_token,  
                            get_current_user)
from app.schemas.member_schema import MemberOut
from beanie import PydanticObjectId


router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister):
    if await Member.find_one(Member.email == user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Email already registered")
    
    new_member = Member(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        phone=user_data.phone,
    )
    new_member.set_password(user_data.password)

    await new_member.insert()

    access_token = create_access_token(data={"sub": str(new_member.id)})
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm=Depends()):
    user = await Member.find_one(Member.email == form_data.username)
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/me", response_model=MemberOut)
async def get_current_user_endpoint(current_user: Member=Depends(get_current_user)):
    return current_user

@router.put("/update-password")
async def update_password(password_data: PasswordUpdate,
                           current_user: Member = Depends(get_current_user)):
    if not current_user.verify_password(password_data.current_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Current password is incorrect"
                            )
    
    current_user.set_password(password_data.new_password)
    await current_user.save()
    return {"message": "Password updated successfully"}
    
@router.post("/logout")
async def logout():
    return {"message": "Logout successful"}