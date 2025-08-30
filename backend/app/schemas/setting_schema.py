from pydantic import BaseModel, HttpUrl

class AttendanceSettingsSchema(BaseModel):
    google_form_url: str


class AttendanceSettingsResponse(BaseModel):
    google_form_url: str

    