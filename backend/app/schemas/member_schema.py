from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str = "Member"


class MemberCreate(BaseModel):
    password: str


class MemberUpdate(BaseModel):
    fisrt_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    ia_active: Optional[bool] = None
    department: Optional[List[str]] = None


class MemberSelfUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class MemberOut(MemberCreate):
    id: str
    join_date: datetime
    is_active: bool
    departments: List[str] = []

    model_config = ConfigDict(from_attributes=True)