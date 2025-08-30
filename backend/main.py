import os
import logging
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from app.database.connection import init_db
from app.middleware import LoggingMiddleware
from app.utils.cache import cache
from app.routes import auth, members, events, attendance, prayer_testimony, announcements
from app.routes.admin import admin_router
from fastapi.middleware.cors import CORSMiddleware



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

origins = [
    "http://localhost:3000",
     # Your frontend on Render here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(members.router, prefix="/members", tags=["Member Profile"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
app.include_router(prayer_testimony.router, prefix="/prayer", tags=["Prayer & Testimony"])
app.include_router(announcements.router, prefix="/announcements", tags=["Announcements"])

# Add middleware for request logging
app.add_middleware(LoggingMiddleware)

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}
logging.config.dictConfig(log_config)






@app.on_event("startup")
async def startup_event():
    """Initialize application services on startup"""
    logger.info("Starting application initialization...")
    
    try:
        await init_db()
        logger.info("Database initialized successfully")
        
        await cache.init()
        logger.info("Cache initialized successfully")
        
        
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

@app.get("/health")
async def health_check():
    return {"status": "healthy"}