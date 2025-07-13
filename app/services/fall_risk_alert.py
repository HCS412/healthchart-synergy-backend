from typing import List
from app.models.alert import Alert
from app.models.room import Room
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

async def check_fall_risk_alert(room: Room, db: AsyncSession) -> List[Alert]:
    alerts = []
    if room.fall_risk:
        alerts.append(Alert(
            type="fall_risk_unattended",
            severity="high",
            room_id=room.id,
            message=f"Fall-risk patient in room {room.id} has no staff present.",
            timestamp=datetime.utcnow()
        ))
    return alerts
