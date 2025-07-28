from fastapi import APIRouter, HTTPException, Depends
from beanie import PydanticObjectId
from app.models.event_model import Event, EventRegistration, VolunteerSignup
from app.schemas.event_schema import EventOut, RegistrationCreate, VolunteerSignupCreate
from app.routes.auth import get_current_user
from app.models.member_model import Member

router = APIRouter(tags=["Events"])

@router.get("/", response_model=list[EventOut])
async def list_upcoming_events():
    # Only published events
    events = await Event.find(Event.is_published == True).sort(Event.start_time).to_list()
    return events

@router.get("/{event_id}", response_model=EventOut)
async def get_event_details(event_id: PydanticObjectId):
    event = await Event.get(event_id)
    if not event or not event.is_published:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/{event_id}/register")
async def rsvp_to_event(event_id: PydanticObjectId, current_user: Member = Depends(get_current_user)):
    event = await Event.get(event_id)
    if not event or not event.is_published:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if not event.registration_required:
        raise HTTPException(status_code=400, detail="Registration not required for this event")
    
    # Check if already registered
    existing_reg = await EventRegistration.find_one(
        EventRegistration.event_id == str(event_id),
        EventRegistration.member_id == str(current_user.id)
    )
    if existing_reg:
        raise HTTPException(status_code=400, detail="Already registered for this event")
    
    # Check capacity
    if event.max_attendees:
        current_registrations = await EventRegistration.find(
            EventRegistration.event_id == str(event_id)
        ).count()
        if current_registrations >= event.max_attendees:
            raise HTTPException(status_code=400, detail="Event is full")
    
    # Create registration
    new_reg = EventRegistration(
        event_id=str(event_id),
        member_id=str(current_user.id)
    )
    await new_reg.insert()
    return {"message": "Successfully registered for event"}



@router.post("/{event_id}/volunteer")
async def signup_to_volunteer(event_id: PydanticObjectId, role: str, current_user: Member = Depends(get_current_user)):
    event = await Event.get(event_id)
    if not event or not event.is_published:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if not event.volunteers_needed:
        raise HTTPException(status_code=400, detail="Volunteers not needed for this event")
    
    if role not in event.volunteer_roles:
        raise HTTPException(status_code=400, detail="Invalid volunteer role")
    
    # Check if already signed up
    existing_signup = await VolunteerSignup.find_one(
        VolunteerSignup.event_id == str(event_id),
        VolunteerSignup.member_id == str(current_user.id),
        VolunteerSignup.role == role
    )
    if existing_signup:
        raise HTTPException(status_code=400, detail="Already signed up for this role")
    
    # Create signup
    new_signup = VolunteerSignup(
        event_id=str(event_id),
        member_id=str(current_user.id),
        role=role
    )
    await new_signup.insert()
    return {"message": "Volunteer signup successful"}