import uuid
from sqlalchemy.orm import Session
from app.models.event import Event, EventDB
from app.models.room import Room
from app.database import SessionLocal
from app.services import room_store

def handle_event(event: Event):
    with SessionLocal() as db:
        # Log event to DB
        db_event = EventDB(
            id=str(uuid.uuid4()),
            type=event.type,
            room_id=event.room_id,
            target_room_id=event.target_room_id,
            patient_name=event.patient_name,
            fall_risk=event.fall_risk,
            isolation=event.isolation,
            timestamp=event.timestamp
        )
        db.add(db_event)
        db.commit()

    # Update room state (same logic as before)
    if event.type == "admit":
        room_store.update_room(Room(
            id=event.room_id,
            status="occupied",
            patient_name=event.patient_name or "Unknown",
            fall_risk=event.fall_risk,
            isolation=event.isolation
        ))
        return {"message": f"Patient admitted to room {event.room_id}"}

    elif event.type == "discharge":
        room_store.update_room(Room(
            id=event.room_id,
            status="vacant",
            patient_name=None,
            fall_risk=False,
            isolation=False
        ))
        return {"message": f"Room {event.room_id} marked as vacant"}

    elif event.type == "transfer":
        room_store.update_room(Room(
            id=event.room_id,
            status="vacant",
            patient_name=None,
            fall_risk=False,
            isolation=False
        ))

        target_id = event.target_room_id or "Unspecified"
        room_store.update_room(Room(
            id=target_id,
            status="occupied",
            patient_name=event.patient_name or "Unknown",
            fall_risk=event.fall_risk,
            isolation=event.isolation
        ))
        return {"message": f"Patient transferred from {event.room_id} to {target_id}"}
