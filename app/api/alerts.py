from fastapi import APIRouter
from typing import List
from app.models.alert import Alert
from app.services.alert_logic import scan_for_alerts, get_alert_history

router = APIRouter()

@router.get("/", response_model=List[Alert])
def get_current_alerts():
    return scan_for_alerts()

@router.get("/history", response_model=List[Alert])
def get_all_alerts():
    return get_alert_history()
