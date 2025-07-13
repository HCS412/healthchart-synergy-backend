from fastapi import FastAPI
from app.api import rooms, events, badges, alerts
from app.database import Base, engine
from app.api import signage


app = FastAPI(
    title="HealthChart Synergy Backend",
    version="0.1.0",
    description="Powers smart signage, badge tracking, room orchestration, and alerts"
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(rooms.router, prefix="/rooms", tags=["Rooms"])
app.include_router(events.router, prefix="/events", tags=["EHR Events"])
app.include_router(badges.router, prefix="/badges", tags=["Badge Reader"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])

@app.get("/")
def root():
    return {"status": "HealthChart Synergy is running"}
