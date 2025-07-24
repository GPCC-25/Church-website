from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId


class UserModel(BaseModel):
    id: Optional[str]
    username: str
    email: EmailStr
    password: str