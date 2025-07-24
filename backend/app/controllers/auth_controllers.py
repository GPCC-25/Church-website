from fastapi import HTTPException
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.auth import hash_password, very_password, create_access_token
from app.database.database import database



async def register_user(user: UserCreate):
    existing_user = await database["users"]. find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)

    result = await database["users"].insert_one(user_dict)
    return {"id": str(result.inserted_id), "email": user.email}



async def login_user(user: UserLogin):
    db_user = await database["user"].find_one({"email": user.email})
    if not db_user or not very_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer"}