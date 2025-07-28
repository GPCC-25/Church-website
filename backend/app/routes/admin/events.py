from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from app.models.event_model import Event, EventRegistration, VolunteerSignup
from app.schemas.event_schema import (EventCreate,
                                      EventUpdate,
                                      EventOut,
                                      RegistrationOut,
                                      VolunteerSignupOut)


router = APIRouter()

@router.post("/", response_model=EventOut)
async def create_event(event_data: EventCreate):
    new_event = Event(**event_data.dict())
    await new_event.insert()
    return new_event



@router.put("/{event_id}", response_model=EventOut)
async def update_event(event_id: PydanticObjectId, event_data: EventUpdate):
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    update_data = event_data.dict(exclude_unset=True)
    await event.set(update_data)
    return event



@router.delete("/{event_id}")
async def delete_event(event_id: PydanticObjectId):
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    await event.delete()
    return {"message", "Event deleted"}


@router.get("/registrations", response_model=list[RegistrationOut])
async def view_event_registration(event_id: str=None):
    query = {}
    if event_id:
        query["event_id"] = event_id
    registrations = await EventRegistration.find(query).to_list()
    return registrations


@router.get("/volunteers", response_model=list[VolunteerSignupOut])
async def view_volunteer_list(event_id: str = None):
    query = {}
    if event_id:
        query["event_id"] = event_id
    volunteers = await VolunteerSignup.find(query).to_list()
    return volunteers