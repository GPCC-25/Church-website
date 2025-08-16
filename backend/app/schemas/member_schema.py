from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Optional, List
from bson import ObjectId

class MemberBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    


class MemberCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str = "Member"
    password: str = Field(..., min_length=8)


class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    department: Optional[List[str]] = None


class MemberSelfUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class MemberOut(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    role: str
    join_date: datetime
    is_active: bool
    departments: List[str] = []
    
    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        from_attributes=True
    )

