from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import List, Optional
from bson import ObjectId



class CommentBase(BaseModel):
    text: str


class CommentOut(CommentBase):
    member_id: str
    created_at: datetime

    @field_validator("member_id", mode="before")
    @classmethod
    def convert_member_id(cls,v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


class PrayerRequestBase(BaseModel):
    content: str
    is_public: bool = True


class PrayerRequestCreate(PrayerRequestBase):
    pass


class PrayerRequestOut(PrayerRequestBase):
    id: str
    member_id: str
    is_approved: bool
    prayer_count: int
    created_at: datetime
    comments: List[CommentOut] = []

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True
    )
    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @field_validator("member_id", mode="before")
    @classmethod
    def convert_member_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


class TestimonyBase(BaseModel):
    content: str


class TestimonyCreate(TestimonyBase):
    pass


class TestimonyOut(TestimonyBase):
    id: str
    member_id: str
    is_approved: bool
    created_at: datetime
    comments: List[CommentOut] = []

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


class PrayerCounterUpdate(BaseModel):
    increment: int = Field(1, ge=1)