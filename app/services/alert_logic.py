from typing import List
from app.models.alert import Alert
from app.services import room_store, badge_store

def scan_for_alerts() -> List[Alert]:
    alerts: List[Alert] = []
    room_map = {r.id: r for r in room_store.get_all_rooms()}
    badge_locations = badge_store.badge_locations

    # Reverse lookup: room_id -> list of staff
    room_staff_map = {}
    for badge_id, room_id in badge_locations.items():
        if room_id:
            room_staff_map.setdefault(room_id, []).append(badge_id)

    for room_id, room in room_map.items():
        staff_present = room_staff_map.get(room_id, [])

        # Alert if fall risk patient and no staff present
        if room.fall_risk and not staff_present:
            alerts.append(Alert(
                type="fall_risk_unattended",
                severity="high",
                room_id=room_id,
                message=f"Fall-risk patient in room {room_id} has no staff present."
            ))

        # Alert if isolation and more than one person in room (demo logic)
        if room.isolation and len(staff_present) > 1:
            alerts.append(Alert(
                type="isolation_breach",
                severity="medium",
                room_id=room_id,
                message=f"Isolation protocol potentially breached in room {room_id}."
            ))

    return alerts
