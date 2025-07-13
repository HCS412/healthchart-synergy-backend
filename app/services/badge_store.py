from typing import Dict, List
from app.models.badge import BadgeEvent

# badge_id -> list of badge events (for audit trail)
badge_logs: Dict[str, List[BadgeEvent]] = {}

# badge_id -> current room or None
badge_locations: Dict[str, str | None] = {}

def record_badge_event(event: BadgeEvent):
    # Track audit trail
    badge_logs.setdefault(event.badge_id, []).append(event)

    # Update location
    if event.type == "in":
        badge_locations[event.badge_id] = event.room_id
    else:
        badge_locations[event.badge_id] = None

    return {"message": f"Badge {event.type} event recorded", "badge_id": event.badge_id}

def get_badge_location(badge_id: str):
    return {"badge_id": badge_id, "location": badge_locations.get(badge_id)}

def get_badge_log(badge_id: str):
    return badge_logs.get(badge_id, [])
