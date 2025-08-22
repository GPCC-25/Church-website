from fastapi import APIRouter, HTTPException, Depends
from app.database.connection import get_db
from app.dependencies import require_admin
from app.models.member_model import VALID_ROLES
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.post("/seed")
async def seed_roles(
    db: AsyncIOMotorDatabase = Depends(get_db),
    admin=Depends(require_admin)
):
    
    roles_collection = db["system_roles"]
    existing = await roles_collection.find_one({"name": "system_roles"})
    
    
    if not existing:
        await roles_collection.insert_one({
            "name": "system_roles", 
            "roles": VALID_ROLES,
            "description": "System-defined roles"
            })
    else:
        existing_roles = existing["roles"]
        new_roles = [role for role in VALID_ROLES if not existing_roles]
    
    if not new_roles:
        return {"message": "No new roles to add"}
    
    updated_roles  = existing_roles + new_roles
    await roles_collection.update_one({
        "name": "system_roles"}, 
        {"$set": {"roles": updated_roles}}
         )
    
    return {"message": "Roles updated successfully",
            "roles": new_roles}