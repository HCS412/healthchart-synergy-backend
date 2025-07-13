from fastapi import APIRouter
from app.models.event import Event
from app.services.event_handler import handle_event

router = APIRouter()

@router.post("/", tags=["EHR Events"])
def post_event(event: Event):
    return handle_event(event)
