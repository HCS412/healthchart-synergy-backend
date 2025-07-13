from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class BadgeEvent(BaseModel):
    badge_id: str
    room_id: str
    type: Literal["in", "out"]
    timestamp: datetime = datetime.utcnow()
