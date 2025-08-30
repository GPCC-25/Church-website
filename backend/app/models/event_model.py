from datetime import datetime
from typing import Optional, List
from beanie import Document
from pydantic import Field

class Event(Document):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    event_type: str = "service"
    is_published: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    registration_required: bool = False
    max_attendees: Optional[int] = None
    volunteers_needed: bool = False
    volunteer_roles: List[str] = [] # e.g ['choir', ''usher]
    
     


    class Setting:
        name = "events"

class EventRegistration(Document):
    event_id: str
    member_id: str
    member_name: str
    role: str
    registration_time: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending" # registered, attended, cancelled

    class Settings:
        name = "event_registrations"


class VolunteerSignup(Document):
    event_id: str
    member_id: str
    member_name: str = Field(default="unknown")
    role: str
    signup_time: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, confirmed, declined
    
    class Settings:
        name = "volunteer_signups"