import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base, engine, get_db
from app.api import rooms, events, badges, alerts, signage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting HealthChart Synergy Backend")

try:
    logger.info("Importing rooms API")
    from app.api import rooms
    logger.info("Importing events API")
    from app.api import events
    logger.info("Importing badges API")
    from app.api import badges
    logger.info("Importing alerts API")
    from app.api import alerts
    logger.info("Importing signage API")
    from app.api import signage
except Exception as e:
    logger.error(f"Failed to import API modules: {e}")
    raise

app = FastAPI(
    title="HealthChart Synergy Backend",
    version="0.1.0",
    description="Powers smart signage, badge tracking, room orchestration, and alerts"
)

@app.on_event("startup")
async def on_startup():
    logger.info("Creating database tables")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

app.include_router(rooms.router, prefix="/rooms", tags=["Rooms"])
app.include_router(events.router, prefix="/events", tags=["EHR Events"])
app.include_router(badges.router, prefix="/badges", tags=["Badge Reader"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
app.include_router(signage.router, prefix="/signage", tags=["Smart Signage"])

@app.get("/")
async def root():
    return {"status": "HealthChart Synergy is running"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
