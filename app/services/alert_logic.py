import uuid
from typing import List
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.alert import Alert, AlertDB
from app.services.room_store import get_all_rooms
from app.services.badge_store import get_badge_locations
from app.services.fall_risk_alert import check_fall_risk_alert
from app.services.isolation_alert import check_isolation_alert

async def scan_for_alerts(db: AsyncSession, background_tasks: BackgroundTasks) -> List[Alert]:
    async def process_alerts():
        alerts = []
        room_map = {r.id: r for r in await get_all_rooms(db)}
        badge_locations = await get_badge_locations(db)

        room_staff_map = {}
        for badge_id, room_id in badge_locations.items():
            if room_id:
                room_staff_map.setdefault(room_id, []).append(badge_id)

        for room_id, room in room_map.items():
            staff_present = room_staff_map.get(room_id, [])
            if room.fall_risk and not staff_present:
                alerts.extend(await check_fall_risk_alert(room, db))
            if room.isolation and len(staff_present) > 1:
                alerts.extend(await check_isolation_alert(room, staff_present, db))

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
        await db.commit()
        return alerts

    background_tasks.add_task(process_alerts)
    return []

async def get_alert_history(db: AsyncSession) -> List[Alert]:
    result = await db.execute("SELECT * FROM alerts ORDER BY timestamp DESC")
    return [Alert(**row) for row in result.mappings().all()]
