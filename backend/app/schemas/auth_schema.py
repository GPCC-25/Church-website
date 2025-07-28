from pydantic import BaseModel, EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


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