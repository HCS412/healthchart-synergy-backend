from fastapi import APIRouter
from typing import List
from app.models.room import Room
from app.services.room_store import get_all_rooms, update_room

router = APIRouter()

@router.get("/rooms", response_model=List[Room])
def get_rooms():
    return get_all_rooms()

@router.post("/rooms/update", response_model=Room)
def update_room_info(room: Room):
    return update_room(room)
