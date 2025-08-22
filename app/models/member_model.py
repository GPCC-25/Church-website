from beanie import Document, Indexed
from pydantic import EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

VALID_ROLES = ["Member", "Usher", "Choir", "Deacon", "Staff", "Admin"]

class Member(Document):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str = "Member"
    join_date: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    departments: List[str] = []
    password_hash: str  

    notification_preference: str = Field("both", description="Preferred notification: email, sms, or both")
    sms_opt_in: bool = Field(False, description="Explicit consent for SMS notifications")


    @validator("role")
    def validate_role(cls, v):
        if v not in VALID_ROLES:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(VALID_ROLES)}")
        return v


    class Settings:
        name = "members"


    def set_password(self, password: str):
        """Hash and set the password"""
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash"""
        return pwd_context.verify(password, self.password_hash)