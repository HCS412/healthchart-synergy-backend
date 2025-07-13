from typing import List
from app.models.alert import Alert
from app.models.room import Room
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

async def check_isolation_alert(room: Room, staff_present: List[str], db: AsyncSession) -> List[Alert]:
    alerts = []
    if room.isolation and len(staff_present) > 1:
        alerts.append(Alert(
            type="isolation_breach",
            severity="medium",
            room_id=room.id,
            message=f"Isolation protocol potentially breached in room {room.id}.",
            timestamp=datetime.utcnow()
        ))
    return alerts
