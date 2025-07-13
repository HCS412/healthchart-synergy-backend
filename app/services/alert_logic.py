import uuid
from typing import List
from app.models.alert import Alert, AlertDB
from app.services import room_store
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services import badge_store

def scan_for_alerts() -> List[Alert]:
    alerts: List[Alert] = []
    room_map = {r.id: r for r in room_store.get_all_rooms()}
    badge_locations = badge_store.get_badge_locations()  # returns badge_id → room_id

    # Reverse lookup: room_id → staff
    room_staff_map = {}
    for badge_id, room_id in badge_locations.items():
        if room_id:
            room_staff_map.setdefault(room_id, []).append(badge_id)

    for room_id, room in room_map.items():
        staff_present = room_staff_map.get(room_id, [])

        if room.fall_risk and not staff_present:
            alerts.append(Alert(
                type="fall_risk_unattended",
                severity="high",
                room_id=room_id,
                message=f"Fall-risk patient in room {room_id} has no staff present."
            ))

        if room.isolation and len(staff_present) > 1:
            alerts.append(Alert(
                type="isolation_breach",
                severity="medium",
                room_id=room_id,
                message=f"Isolation protocol potentially breached in room {room_id}."
            ))

    # Save alerts to DB
    with SessionLocal() as db:
        for alert in alerts:
            db_alert = AlertDB(
                id=str(uuid.uuid4()),
                type=alert.type,
                severity=alert.severity,
                room_id=alert.room_id,
                message=alert.message,
                timestamp=alert.timestamp
            )
            db.add(db_alert)
        db.commit()

    return alerts

def get_alert_history() -> List[AlertDB]:
    with SessionLocal() as db:
        return db.query(AlertDB).order_by(AlertDB.timestamp.desc()).all()
