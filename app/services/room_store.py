from typing import Dict
from app.models.room import Room

# In-memory room store
room_store: Dict[str, Room] = {
    "101": Room(id="101", status="occupied", fall_risk=True, isolation=False),
    "102": Room(id="102", status="vacant", fall_risk=False, isolation=False)
}

def get_all_rooms():
    return list(room_store.values())

def update_room(room: Room):
    room_store[room.id] = room
    return room
