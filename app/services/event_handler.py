from app.models.event import Event
from app.models.room import Room
from app.services import room_store

def handle_event(event: Event) -> dict:
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
        # Mark current room vacant
        room_store.update_room(Room(
            id=event.room_id,
            status="vacant",
            patient_name=None,
            fall_risk=False,
            isolation=False
        ))

        # Occupy target room
        target_id = event.target_room_id or "Unspecified"
        room_store.update_room(Room(
            id=target_id,
            status="occupied",
            patient_name=event.patient_name or "Unknown",
            fall_risk=event.fall_risk,
            isolation=event.isolation
        ))
        return {"message": f"Patient transferred from {event.room_id} to {target_id}"}

    else:
        return {"error": "Unknown event type"}
