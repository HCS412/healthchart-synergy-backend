from sqlalchemy import Column, String, DateTime
from app.database import Base
from pydantic import BaseModel
from typing import Literal
from datetime import datetime

# SQLAlchemy model
class AlertDB(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    severity = Column(String)
    room_id = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Pydantic model
class Alert(BaseModel):
    type: Literal["fall_risk_unattended", "isolation_breach"]
    severity: Literal["low", "medium", "high"]
    room_id: str
    message: str
    timestamp: datetime = datetime.utcnow()

    class Config:
        from_attributes = True
