from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.member_model import Member
from app.schemas.auth_schema import TokenResponse, UserRegister, PasswordUpdate
from app.utils.auth import (create_access_token,  
                            verify_password,
                            get_password_hash,
                            get_current_active_user
                        )
from app.schemas.member_schema import MemberOut, MemberCreate, MemberSelfUpdate
from app.schemas.auth_schema import TokenResponse, PasswordUpdate
import logging
from bson import ObjectId


logger = logging.getLogger(__name__)
router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(user_data: MemberCreate):
    if await Member.find_one(Member.email == user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Email already registered")
    
    hashed_password = get_password_hash(user_data.password)
    new_member = Member(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hashed_password,
        role = user_data.role
    )
    await new_member.insert()
    access_token = create_access_token(data={"sub": str(new_member.id)})


    member_out = MemberOut(
        id=str(new_member.id),
        first_name=new_member.first_name,
        last_name=new_member.last_name,
        email=new_member.email,
        phone=new_member.phone,
        role=new_member.role,
        join_date=new_member.join_date,
        is_active=new_member.is_active,
        departments=new_member.departments
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": member_out
    }


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm=Depends()):
    
    user = await Member.find_one(Member.email == form_data.username)
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    member_out = MemberOut(
        id=str(user.id),
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        role=user.role,
        join_date=user.join_date,
        is_active=user.is_active,
        departments=user.departments
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": member_out
    }



@router.get("/me", response_model=MemberOut)
async def get_current_user_endpoint(current_user: Member = Depends(get_current_active_user)):
    
    return MemberOut(
        id=str(current_user.id),
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        phone=current_user.phone,
        role=current_user.role,
        join_date=current_user.join_date,
        is_active=current_user.is_active,
        departments=current_user.departments
    )



@router.put("/update-password")
async def update_password(password_data: PasswordUpdate,
                           current_user: Member = Depends(get_current_active_user)
                           ):
    
    
    user = await Member.get(ObjectId(current_user["id"]))
    
    if not verify_password(password_data.current_password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Current password is incorrect"
                            )
    
    new_hashed_password = get_password_hash(password_data.new_password)
    user.password_hash = new_hashed_password
    await user.save()
    return {"messsage": "Password updated successfully"}
    


@router.put("/me", response_model=MemberOut)
async def update_current_user(
    update_data: MemberSelfUpdate,
    current_user: Member = Depends(get_current_active_user)
):
    # Apply updates
    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(current_user, field, value)
    
    # Save changes
    await current_user.save()

    return MemberOut(
        id=str(current_user.id),
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        phone=current_user.phone,
        role=current_user.role,
        join_date=current_user.join_date,
        is_active=current_user.is_active,
        departments=current_user.departments
    )

 
    
@router.post("/logout")
async def logout():
    return {"message": "Logout successful"}