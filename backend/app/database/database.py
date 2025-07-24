from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

MONGO_DEATAILS = config("MONGO_URL")

client = AsyncIOMotorClient(MONGO_DEATAILS)
database = client["church_db"]

def get_database():
    return database