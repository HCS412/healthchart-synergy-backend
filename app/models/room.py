from pydantic import BaseModel

class Room(BaseModel):
    id: str
    status: str  # could be "occupied", "vacant", "cleaning", etc.
    fall_risk: bool
    isolation: bool = False  # optional, defaults to False
