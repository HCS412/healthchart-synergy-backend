from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class Alert(BaseModel):
    type: Literal["fall_risk_unattended", "isolation_breach"]
    severity: Literal["low", "medium", "high"]
    room_id: str
    message: str
    timestamp: datetime = datetime.utcnow()
