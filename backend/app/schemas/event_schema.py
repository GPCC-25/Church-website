from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional


class EventBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    event_type: str
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


class EventOut(EventBase):
    id: str
    is_published: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RegistrationBase(BaseModel):
    event_id: str
    member_id: str


class RegistrationCreate(RegistrationBase):
    pass 


class RegistrationOut(RegistrationBase):
    id: str
    registration_time: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)

class VolunteerSignupBase(BaseModel):
    event_id: str
    member_id: str
    role: str

class VolunteerSignupCreate(VolunteerSignupBase):
    pass 

class VolunteerSignupOut(VolunteerSignupBase):
    id: str
    signup_time: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)
        