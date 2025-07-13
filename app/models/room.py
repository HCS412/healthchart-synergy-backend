from sqlalchemy import Column, String, Boolean
from app.database import Base
from pydantic import BaseModel
from typing import Optional

# SQLAlchemy model
class RoomDB(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, index=True)
    status = Column(String)
    fall_risk = Column(Boolean, default=False)
    isolation = Column(Boolean, default=False)
    patient_name = Column(String, nullable=True)

# Pydantic model
class Room(BaseModel):
    id: str
    status: str
    fall_risk: bool = False
    isolation: bool = False
    patient_name: Optional[str] = None

    class Config:
        orm_mode = True
