from fastapi import APIRouter, Depends, BackgroundTasks
from app.models.event import Event
from app.models.user import User
from app.services.event_handler import handle_event
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth import get_current_user_with_role

router = APIRouter()

@router.post("/", tags=["EHR Events"])
async def post_event(event: Event, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_with_role("admin"))):
    return await handle_event(event, db, background_tasks)
