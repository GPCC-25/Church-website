from pydantic import BaseModel, EmailStr
from app.schemas.member_schema import MemberOut


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: MemberOut


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(UserLogin):
    first_name: str
    last_name: str
    phone: str = None
    

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str