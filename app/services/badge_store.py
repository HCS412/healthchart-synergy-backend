import uuid
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.badge import BadgeEvent, BadgeEventDB

async def record_badge_event(db: AsyncSession, event: BadgeEvent):
    event_id = str(uuid.uuid4())
    await db.execute(
        """
        INSERT INTO badge_events (id, badge_id, room_id, type, timestamp)
        VALUES (:id, :badge_id, :room_id, :type, :timestamp)
        """,
        {
            "id": event_id,
            "badge_id": event.badge_id,
            "room_id": event.room_id,
            "type": event.type,
            "timestamp": event.timestamp
        }
    )
    await db.commit()
    return {"message": f"Badge {event.type} recorded", "badge_id": event.badge_id}

async def get_badge_locations(db: AsyncSession) -> Dict[str, str]:
    result = await db.execute(
        """
        SELECT DISTINCT ON (badge_id) badge_id, room_id, type, timestamp
        FROM badge_events
        ORDER BY badge_id, timestamp DESC
        """
    )
    badge_locations = {}
    for row in result.mappings():
        if row["type"] == "in":
            badge_locations[row["badge_id"]] = row["room_id"]
    return badge_locations

async def get_badge_log(db: AsyncSession, badge_id: str) -> List[BadgeEvent]:
    result = await db.execute(
        """
        SELECT * FROM badge_events
        WHERE badge_id = :badge_id
        ORDER BY timestamp DESC
        """,
        {"badge_id": badge_id}
    )
    return [BadgeEvent(**row) for row in result.mappings().all()]
