import uuid
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import Event, EventDB
from app.models.room import Room
from app.services.room_store import update_room

async def handle_event(event: Event, db: AsyncSession, background_tasks: BackgroundTasks):
    async def process_event():
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
        await db.commit()

        if event.type == "admit":
            await update_room(db, Room(
                id=event.room_id,
                status="occupied",
                patient_name=event.patient_name or "Unknown",
                fall_risk=event.fall_risk,
                isolation=event.isolation
            ))
        elif event.type == "discharge":
            await update_room(db, Room(
                id=event.room_id,
                status="vacant",
                patient_name=None,
                fall_risk=False,
                isolation=False
            ))
        elif event.type == "transfer":
            await update_room(db, Room(
                id=event.room_id,
                status="vacant",
                patient_name=None,
                fall_risk=False,
                isolation=False
            ))
            target_id = event.target_room_id or "Unspecified"
            await update_room(db, Room(
                id=target_id,
                status="occupied",
                patient_name=event.patient_name or "Unknown",
                fall_risk=event.fall_risk,
                isolation=event.isolation
            ))

    background_tasks.add_task(process_event)
    return {"message": "Event processing started"}
