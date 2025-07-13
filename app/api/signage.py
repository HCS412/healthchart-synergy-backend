from fastapi import APIRouter, HTTPException
from app.services import room_store, badge_store, alert_logic
from app.models.room import Room
from app.models.alert import Alert

router = APIRouter()

@router.get("/{room_id}")
def get_room_signage(room_id: str):
    room = room_store.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Get current staff in the room
    badge_locations = badge_store.get_badge_locations()
    staff_in_room = [badge_id for badge_id, r_id in badge_locations.items() if r_id == room_id]

    # Get alerts for this room
    alerts = alert_logic.get_alert_history()
    room_alerts = [a for a in alerts if a.room_id == room_id]

    return {
        "room": room,
        "staff": staff_in_room,
        "alerts": room_alerts
    }
