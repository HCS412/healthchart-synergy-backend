from fastapi import APIRouter, Depends, BackgroundTasks
from typing import List
from app.models.alert import Alert
from app.models.user import User
from app.services.alert_logic import scan_for_alerts, get_alert_history
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth import get_current_user_with_role

router = APIRouter()

@router.get("/", response_model=List[Alert])
async def get_current_alerts(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_with_role("nurse"))):
    return await scan_for_alerts(db, background_tasks)

@router.get("/history", response_model=List[Alert])
async def get_all_alerts(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_with_role("nurse"))):
    return await get_alert_history(db)
