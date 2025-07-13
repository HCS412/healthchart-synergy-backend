from sqlalchemy import Column, String, DateTime
from app.database import Base
from pydantic import BaseModel
from typing import Literal
from datetime import datetime

# SQLAlchemy model
class BadgeEventDB(Base):
    __tablename__ = "badge_events"

    id = Column(String, primary_key=True, index=True)
    badge_id = Column(String, index=True)
    room_id = Column(String)
    type = Column(String)  # "in" or "out"
    timestamp = Column(DateTime, default=datetime.utcnow)

# Pydantic model
class BadgeEvent(BaseModel):
    badge_id: str
    room_id: str
    type: Literal["in", "out"]
    timestamp: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
