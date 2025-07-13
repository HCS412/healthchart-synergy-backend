from typing import Dict, List
from app.models.room import Room

# In-memory store of rooms
room_store: Dict[str, Room] = {}

def get_all_rooms() -> List[Room]:
    return list(room_store.values())

def get_room_by_id(room_id: str) -> Room | None:
    return room_store.get(room_id)

def update_room(room: Room) -> Room:
    room_store[room.id] = room
    return room

def delete_room(room_id: str) -> bool:
    if room_id in room_store:
        del room_store[room_id]
        return True
    return False

def clear_all_rooms():
    room_store.clear()
