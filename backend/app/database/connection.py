import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from beanie import init_beanie


db: AsyncIOMotorDatabase = None

async def init_db():
    global db
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    
    # Extract database name from URI
    if "/" in MONGO_URI:
        db_name = MONGO_URI.split("/")[-1].split("?")[0]
    else:
        db_name = "gpcc_db"
    

    client = AsyncIOMotorClient(MONGO_URI)
    db = client[db_name]
    
    
    await init_beanie(
        database=db,
        document_models=[
            "app.models.member_model.Member",
            "app.models.event_model.Event",
            "app.models.event_model.EventRegistration",
            "app.models.event_model.VolunteerSignup"
        ]
    )
    
    print(f"Connected to MongoDB: {MONGO_URI}")
    print(f"Using database: {db_name}")
    return db

def get_db() -> AsyncIOMotorDatabase:
    """Dependency to get database instance"""
    if db is None:
        raise RuntimeError("Database not initialized")
    return db