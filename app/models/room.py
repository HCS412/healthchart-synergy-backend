from pydantic import BaseModel
from typing import Optional

class Room(BaseModel):
    id: str
    status: str  # "occupied", "vacant", "cleaning", etc.
    fall_risk: bool = False
    isolation: bool = False
    patient_name: Optional[str] = None
