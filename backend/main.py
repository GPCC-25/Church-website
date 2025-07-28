import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import main_router
from app.database.connection import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        # Application will still start without database
        logger.warning("Starting application without database connection")
        app.state.db_initialized = False
    else:
        logger.info("Database initialized successfully")
        app.state.db_initialized = True

# Include routers
app.include_router(main_router)

@app.get("/")
def health_check():
    if app.state.db_initialized:
        return {"status": "ok", "database": "connected"}
    return {"status": "warning", "database": "disconnected"}

@app.get("/test-db")
async def test_db():
    if not app.state.db_initialized:
        return {"status": "error", "message": "Database not initialized"}
    
