from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.member_model import Member
from app.schemas.member_schema import MemberCreate, MemberUpdate, MemberOut
from beanie import PydanticObjectId

router = APIRouter()


@router.get("/", response_model=list[MemberOut])
async def get_all_members():
    return await Member.find_all().to_list()


@router.post("/", response_model=MemberOut)
async def create_member(member_data: MemberCreate):
    if await Member.find_one(Member.email == member_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_member = Member(**member_data.dict())
    await new_member.insert()
    return new_member


@router.put("/{member_id}", response_model=MemberOut)
async def update_member(member_id: PydanticObjectId, update_data:MemberUpdate):
    member = await Member.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    update_data = update_data.dict(exclude_unset=True)
    await member.set(update_data)
    return member


@router.delete("/{member_id}")
async def delete_member(member_id: PydanticObjectId):
    member = await Member.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Memebr not found")
    
    await member.delete()
    return {"message": "Member deleted"}


@router.get("/search")
async def search_members(role: str = Query(None)):
    if not role:
        raise HTTPException(status_code=400, detail="Role parameter required")
    members = await Member.find(Member.role == role).to_list()
    return members






