from fastapi import APIRouter, HTTPException
from app.models.badge import BadgeEvent
from app.services import badge_store

router = APIRouter()

@router.post("/", tags=["Badge Reader"])
def badge_event(event: BadgeEvent):
    return badge_store.record_badge_event(event)

@router.get("/{badge_id}/location", tags=["Badge Reader"])
def current_location(badge_id: str):
    return badge_store.get_badge_location(badge_id)

@router.get("/{badge_id}/log", tags=["Badge Reader"])
def badge_log(badge_id: str):
    log = badge_store.get_badge_log(badge_id)
    if not log:
        raise HTTPException(status_code=404, detail="No badge history found")
    return log
