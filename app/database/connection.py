import os
import logging
import certifi
import ssl
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

logger = logging.getLogger(__name__)

# Global database instance
db = None

async def init_db():
    global db
    try:
        # Get MongoDB URI from environment variables
        MONGO_URI = os.getenv("MONGO", "mongodb://localhost:27017/church_app")
        logger.info(f"Using MongoDB URI: {MONGO_URI}")
        
        # Extract database name
        if "/" in MONGO_URI:
            db_name = MONGO_URI.split("/")[-1].split("?")[0]
            if db_name == "":
                db_name = "gpcc_db"
        else:
            db_name = "gpcc_db"
        logger.info(f"Using database: {db_name}")
        
        # Create a custom SSL context for Python 3.13 compatibility
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.load_verify_locations(certifi.where())
        
        # Create client with explicit SSL context
        client = AsyncIOMotorClient(
            MONGO_URI,
            serverSelectionTimeoutMS=20000,
            tlsCAFile=certifi.where(),
            tlsAllowInvalidCertificates=True,
        )
        
        # Get database
        db = client[db_name]
        
        # Initialize Beanie
        await init_beanie(
            database=db,
            document_models=[
                "app.models.member_model.Member",
                "app.models.event_model.Event",
                "app.models.event_model.EventRegistration",
                "app.models.event_model.VolunteerSignup",
                "app.models.prayer_testimony_model.PrayerRequest",
                "app.models.prayer_testimony_model.Testimony",
                "app.models.settings_model.AttendanceSettings",
                "app.models.announcement_model.Announcement"
            ]
        )
        
        # Test connection
        await client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        return db
    except Exception as e:
        logger.exception("MongoDB connection failed")
        # Suggest additional troubleshooting steps
        logger.error("If connection persists, try these additional steps:")
        logger.error("1. Ensure your IP is whitelisted in MongoDB Atlas")
        logger.error("2. Check firewall settings to allow outbound connections on port 27017")
        logger.error("3. Try updating your root certificates: pip install --upgrade certifi")
        logger.error("4. Temporarily try with tlsAllowInvalidCertificates=True for testing")
        raise

def get_db():
    if db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return db