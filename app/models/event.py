from pydantic import BaseModel
from typing import Literal, Optional

class Event(BaseModel):
    type: Literal["admit", "discharge", "transfer"]
    room_id: str
    patient_name: Optional[str] = None  # required for admit/transfer
    fall_risk: Optional[bool] = False
    isolation: Optional[bool] = False
    target_room_id: Optional[str] = None  # only used for transfer
