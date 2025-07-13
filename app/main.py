from fastapi import FastAPI
from app.api import rooms, events, badges, alerts, signage
from app.database import Base, engine

app = FastAPI(
    title="HealthChart Synergy Backend",
    version="0.1.0",
    description="Powers smart signage, badge tracking, room orchestration, and alerts"
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(rooms.router, prefix="/rooms", tags=["Rooms"])
app.include_router(events.router, prefix="/events", tags=["EHR Events"])
app.include_router(badges.router, prefix="/badges", tags=["Badge Reader"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
app.include_router(signage.router, prefix="/signage", tags=["Smart Signage"])

@app.get("/")
async def root():
    return {"status": "HealthChart Synergy is running"}
