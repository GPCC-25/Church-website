from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from typing import List, Optional
from beanie import PydanticObjectId

class EventBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    is_published: bool = False
    event_type: str = Field("service", pattern="^(service|meeting|outreach|conference|ceremony|revival)$")
    registration_required: bool
    max_attendees: Optional[int] = None
    volunteers_needed: bool
    volunteer_roles: List[str] = []


class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    event_type: Optional[str] = None
    is_published: Optional[bool] = None
    registration_required: Optional[bool] = None
    max_attendees: Optional[int] = None
    volunteers_needed: Optional[bool] = None
    volunteer_roles: Optional[List[str]] = None


class EventReminderSettings(BaseModel):
    reminders_enabled: bool
    reminder_days_before: Optional[int] = Field(1, ge=0, le=7)




class EventOut(EventBase):
    id: str
    
    

    model_config = ConfigDict(from_attributes=True)


class RegistrationBase(BaseModel):
    event_id: str
    member_id: str
    member_name: str


class RegistrationCreate(RegistrationBase):
    pass 


class RegistrationOut(RegistrationBase):
    id: str
    registration_time: datetime = Field(default_factory=datetime.utcnow)
    status: str

    @field_validator("id", "event_id", "member_id", mode="before")
    def convert_ids(cls, value):
        if isinstance(value, PydanticObjectId):
            return str(value)
        return value
    
    model_config = ConfigDict(from_attributes=True)


class VolunteerSignupBase(BaseModel):
    event_id: str
    member_id: str
    role: str


class VolunteerSignupCreate(VolunteerSignupBase):
    pass 


class VolunteerSignupOut(VolunteerSignupBase):
    member_name: str
    id: str
    signup_time: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)
        