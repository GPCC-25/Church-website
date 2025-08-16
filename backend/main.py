import os
import logging
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from app.database.connection import init_db
from app.middleware import LoggingMiddleware
from app.utils.cache import cache
from app.database.connection import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.routes import auth, members, events, attendance, prayer_testimony
from app.routes.admin import admin_router



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger(__name__)


load_dotenv()
logger.info("Environment variables loaded")

app = FastAPI(
    title="Church Management System API",
    description="Backend API for church management application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(members.router, prefix="/members", tags=["Member Profile"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
app.include_router(prayer_testimony.router, prefix="/prayer", tags=["Prayer & Testimony"])

# Add middleware for request logging
app.add_middleware(LoggingMiddleware)

@app.on_event("startup")
async def startup_event():
    """Initialize application services on startup"""
    logger.info("Starting application initialization...")
    
    try:
        await init_db()
        logger.info("Database initialized successfully")
        
        await cache.init()
        logger.info("Cache initialized successfully")
        
        await create_initial_admin()
        
    except Exception as e:
        logger.exception(f"Application initialization failed: {str(e)}")
        raise
    else:
        logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down application...")
    await cache.close()
    logger.info("Cache closed successfully")



@app.get("/", include_in_schema=False)
def health_check():
    """Basic health check endpoint"""
    return {
        "status": "ok",
        "message": "Church Management API is running",
        "version": app.version
    }

@app.get("/test-db")
async def test_db(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Test database connection endpoint"""
    try:
        collections = await db.list_collection_names()
        return {
            "status": "success",
            "collections": collections,
            "count": len(collections)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def create_initial_admin():
    """Create initial admin user if no users exist"""
    from app.models.member_model import Member
    from app.utils.auth import get_password_hash
    from app.database.connection import get_db
    
    
    admin_email = os.getenv("INITIAL_ADMIN_EMAIL", "admin@church.org")
    admin_password = os.getenv("INITIAL_ADMIN_PASSWORD", "SecurePassword123!")
    
    
    existing_admin = await Member.find_one({"role": "Admin", "is_active": True})
    if existing_admin:
        logger.info("Admin user already exists")
        return
    
    existing_user = await Member.find_one({"email": admin_email})
    if existing_user:
        logger.info("Initial admin user already exists")
    
    # Create admin user
    password_hashed = get_password_hash(admin_password)

    admin_user = Member(
        first_name="John",
        last_name="Doe",
        email=admin_email,
        phone="+1234567890",
        role="Admin",
        is_active=True,
        password_hash= password_hashed
    )
    await admin_user.create()
    
    logger.info(f"Created initial admin user: {admin_email}, {admin_user.role}, {admin_user.is_active}, {admin_user.first_name}")