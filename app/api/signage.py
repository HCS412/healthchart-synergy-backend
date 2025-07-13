from fastapi import APIRouter, Depends, HTTPException
from app.services.room_store import get_all_rooms, get_room_by_id
from app.services.badge_store import get_badge_locations
from app.models.room import Room
from app.models.alert import Alert
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

router = APIRouter()

@router.get("/{room_id}")
async def get_room_signage(room_id: str, db: AsyncSession = Depends(get_db)):
    room = await get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    badge_locations = await get_badge_locations(db)
    staff_in_room = [badge_id for badge_id, r_id in badge_locations.items() if r_id == room_id]

    result = await db.execute(
        "SELECT * FROM alerts WHERE room_id = :room_id",
        {"room_id": room_id}
    )
    room_alerts = [Alert(**row) for row in result.mappings().all()]

    return {
        "room": room,
        "staff": staff_in_room,
        "alerts": room_alerts
    }

@router.get("/all")
async def get_all_signage(db: AsyncSession = Depends(get_db)):
    rooms = await get_all_rooms(db)
    badge_locations = await get_badge_locations(db)
    result = await db.execute("SELECT * FROM alerts")
    alerts = [Alert(**row) for row in result.mappings().all()]

    signage_data = []
    for room in rooms:
        staff_in_room = [badge_id for badge_id, r_id in badge_locations.items() if r_id == room.id]
        room_alerts = [a for a in alerts if a.room_id == room.id]
        signage_data.append({
            "room": room,
            "staff": staff_in_room,
            "alerts": room_alerts
        })
    return signage_data
