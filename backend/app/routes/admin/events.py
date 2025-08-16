from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from app.models.event_model import Event, EventRegistration, VolunteerSignup
from app.schemas.event_schema import (EventCreate,
                                      EventUpdate,
                                      EventOut,
                                      RegistrationOut,
                                      VolunteerSignupOut)
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=EventOut)
async def create_event(event_data: EventCreate):
    new_event = Event(**event_data.dict())
    
    await new_event.insert()

    event_dict = new_event.dict()
    event_dict["id"] = str(event_dict["id"])
    
    # Return the response model with converted ID
    return EventOut(**event_dict)



@router.put("/{event_id}", response_model=EventOut)
async def update_event(event_id: PydanticObjectId, event_data: EventUpdate):
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update the event
    update_data = event_data.dict(exclude_unset=True)
    await event.set(update_data)
    
    # Convert to dict and handle ID
    event_dict = event.dict()
    event_dict["id"] = str(event_dict["id"])
    
    return EventOut(**event_dict)



@router.delete("/{event_id}")
async def delete_event(event_id: PydanticObjectId):
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    await event.delete()
    return {"message": "Event deleted"}



@router.get("/registrations", response_model=list[RegistrationOut])
async def view_event_registration(event_id: PydanticObjectId):
    event_id_str = str(event_id)

    registrations = await EventRegistration.find(
        EventRegistration.event_id == event_id_str
    ).to_list()

    for reg in registrations:
        reg.id = str(reg.id)

    return registrations



@router.get("/volunteers", response_model=list[VolunteerSignupOut])
async def view_volunteer_list(event_id: str = None):
    try:
        event_id_str = str(event_id)

        volunteers = await VolunteerSignup.find(VolunteerSignup.event_id == event_id_str).to_list()
        for vol in volunteers:
            if not isinstance(vol.id, str):
                vol.id = str(vol.id)
        return volunteers
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving volunteers: {str(e)}"
        )