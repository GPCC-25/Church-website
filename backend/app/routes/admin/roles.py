from fastapi import APIRouter, HTTPException, Depends
from app.models.member_model import VALID_ROLES
from app.database.connection import get_db
from app.dependencies import require_admin
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()


@router.post("/seed")
async def seed_roles(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Initialize system roles by creating a document with valid roles.
    This can be extended to include permissions in the future.
    """
    roles_collection = db["system_roles"]
    
    # Check if roles already exist
    existing = await roles_collection.find_one({"name": "system_roles"})
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Roles already initialized"
        )
    
    # Insert valid roles
    await roles_collection.insert_one({
        "name": "system_roles",
        "roles": VALID_ROLES,
        "description": "System-defined roles"
    })
    
    return {"message": "Roles initialized successfully"}