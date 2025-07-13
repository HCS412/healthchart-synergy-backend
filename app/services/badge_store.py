import uuid
from sqlalchemy.orm import Session
from app.models.badge import BadgeEventDB, BadgeEvent
from app.database import SessionLocal

def record_badge_event(event: BadgeEvent):
    with SessionLocal() as db:
        event_id = str(uuid.uuid4())
        db_event = BadgeEventDB(
            id=event_id,
            badge_id=event.badge_id,
            room_id=event.room_id,
            type=event.type,
            timestamp=event.timestamp
        )
        db.add(db_event)
        db.commit()
        return {"message": f"Badge {event.type} recorded", "badge_id": event.badge_id}

def get_badge_location(badge_id: str):
    with SessionLocal() as db:
        event = (
            db.query(BadgeEventDB)
            .filter(BadgeEventDB.badge_id == badge_id)
            .order_by(BadgeEventDB.timestamp.desc())
            .first()
        )
        return {"badge_id": badge_id, "location": event.room_id if event and event.type == "in" else None}

def get_badge_log(badge_id: str):
    with SessionLocal() as db:
        return (
            db.query(BadgeEventDB)
            .filter(BadgeEventDB.badge_id == badge_id)
            .order_by(BadgeEventDB.timestamp.desc())
            .all()
        )
