from fastapi import APIRouter, Depends, HTTPException
from app.models.badge import BadgeEvent
from app.models.user import User
from app.services.badge_store import record_badge_event, get_badge_locations, get_badge_log
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth import get_current_user_with_role

router = APIRouter()

@router.post("/", tags=["Badge Reader"])
async def badge_event(event: BadgeEvent, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_with_role("nurse"))):
    return await record_badge_event(db, event)

@router.get("/{badge_id}/location", tags=["Badge Reader"])
async def current_location(badge_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_with_role("nurse"))):
    locations = await get_badge_locations(db)
    return {"badge_id": badge_id, "location": locations.get(badge_id)}

@router.get("/{badge_id}/log", tags=["Badge Reader"])
async def badge_log(badge_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_with_role("nurse"))):
    log = await get_badge_log(db, badge_id)
    if not log:
        raise HTTPException(status_code=404, detail="No badge history found")
    return log
