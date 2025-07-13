from fastapi import APIRouter
from typing import List
from app.models.room import Room

router = APIRouter()

@router.get("/rooms", response_model=List[Room])
def get_rooms():
    return [
        Room(id="101", status="occupied", fall_risk=True, isolation=True),
        Room(id="102", status="vacant", fall_risk=False),
        Room(id="103", status="cleaning", fall_risk=False)
    ]
