from fastapi import APIRouter, HTTPException
from typing import List
from app.models.room import Room
from app.services import room_store

router = APIRouter()

@router.get("/", response_model=List[Room])
def get_rooms():
    return room_store.get_all_rooms()

@router.get("/{room_id}", response_model=Room)
def get_room(room_id: str):
    room = room_store.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.post("/", response_model=Room)
def create_or_update_room(room: Room):
    return room_store.update_room(room)

@router.delete("/{room_id}", status_code=204)
def delete_room(room_id: str):
    if not room_store.delete_room(room_id):
        raise HTTPException(status_code=404, detail="Room not found")

@router.post("/clear", status_code=204)
def clear_rooms():
    room_store.clear_all_rooms()
