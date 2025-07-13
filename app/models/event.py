from sqlalchemy import Column, String, Boolean, DateTime
from app.database import Base
from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

# SQLAlchemy model
class EventDB(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    type = Column(String)  # "admit", "discharge", "transfer"
    room_id = Column(String)
    target_room_id = Column(String, nullable=True)
    patient_name = Column(String, nullable=True)
    fall_risk = Column(Boolean, default=False)
    isolation = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Pydantic model
class Event(BaseModel):
    type: Literal["admit", "discharge", "transfer"]
    room_id: str
    patient_name: Optional[str] = None
    fall_risk: Optional[bool] = False
    isolation: Optional[bool] = False
    target_room_id: Optional[str] = None
    timestamp: datetime = datetime.utcnow()

    class Config:
        from_attributes = True
