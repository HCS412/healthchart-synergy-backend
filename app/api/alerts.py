from fastapi import APIRouter, Depends, BackgroundTasks
from typing import List
from app.models.alert import Alert
from app.services.alert_logic import scan_for_alerts, get_alert_history
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[Alert])
async def get_current_alerts(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    return await scan_for_alerts(db, background_tasks)

@router.get("/history", response_model=List[Alert])
async def get_all_alerts(db: AsyncSession = Depends(get_db)):
    return await get_alert_history(db)
