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

def get_badge_locations():
    with SessionLocal() as db:
        from app.models.badge import BadgeEventDB
        # Latest badge event per badge_id
        subquery = (
            db.query(
                BadgeEventDB.badge_id,
                BadgeEventDB.room_id,
                BadgeEventDB.type,
                BadgeEventDB.timestamp
            )
            .order_by(BadgeEventDB.badge_id, BadgeEventDB.timestamp.desc())
            .distinct(BadgeEventDB.badge_id)
        )
        badge_locations = {}
        for row in subquery:
            if row.type == "in":
                badge_locations[row.badge_id] = row.room_id
        return badge_locations

def get_badge_log(badge_id: str):
    with SessionLocal() as db:
        return (
            db.query(BadgeEventDB)
            .filter(BadgeEventDB.badge_id == badge_id)
            .order_by(BadgeEventDB.timestamp.desc())
            .all()
        )
