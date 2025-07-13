from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.room import Room, RoomDB

async def get_all_rooms(db: AsyncSession) -> List[Room]:
    result = await db.execute("SELECT * FROM rooms")
    return [Room(**row) for row in result.mappings().all()]

async def get_room_by_id(db: AsyncSession, room_id: str) -> Room | None:
    result = await db.execute("SELECT * FROM rooms WHERE id = :id", {"id": room_id})
    row = result.mappings().first()
    return Room(**row) if row else None

async def update_room(db: AsyncSession, room: Room) -> Room:
    db_room = await db.execute("SELECT * FROM rooms WHERE id = :id", {"id": room.id})
    db_room = db_room.mappings().first()
    if db_room:
        await db.execute(
            """
            UPDATE rooms
            SET status = :status, fall_risk = :fall_risk, isolation = :isolation, patient_name = :patient_name
            WHERE id = :id
            """,
            {
                "id": room.id,
                "status": room.status,
                "fall_risk": room.fall_risk,
                "isolation": room.isolation,
                "patient_name": room.patient_name
            }
        )
    else:
        await db.execute(
            """
            INSERT INTO rooms (id, status, fall_risk, isolation, patient_name)
            VALUES (:id, :status, :fall_risk, :isolation, :patient_name)
            """,
            {
                "id": room.id,
                "status": room.status,
                "fall_risk": room.fall_risk,
                "isolation": room.isolation,
                "patient_name": room.patient_name
            }
        )
    await db.commit()
    result = await db.execute("SELECT * FROM rooms WHERE id = :id", {"id": room.id})
    return Room(**result.mappings().first())

async def delete_room(db: AsyncSession, room_id: str) -> bool:
    result = await db.execute("SELECT * FROM rooms WHERE id = :id", {"id": room_id})
    if result.mappings().first():
        await db.execute("DELETE FROM rooms WHERE id = :id", {"id": room_id})
        await db.commit()
        return True
    return False

async def clear_all_rooms(db: AsyncSession):
    await db.execute("DELETE FROM rooms")
    await db.commit()
