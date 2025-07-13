from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.room import Room
from app.services.room_store import get_all_rooms, get_room_by_id, update_room, delete_room, clear_all_rooms
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[Room])
async def get_rooms(db: AsyncSession = Depends(get_db)):
    return await get_all_rooms(db)

@router.get("/{room_id}", response_model=Room)
async def get_room(room_id: str, db: AsyncSession = Depends(get_db)):
    room = await get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.post("/", response_model=Room)
async def create_or_update_room(room: Room, db: AsyncSession = Depends(get_db)):
    return await update_room(db, room)

@router.delete("/{room_id}", status_code=204)
async def delete_room(room_id: str, db: AsyncSession = Depends(get_db)):
    if not await delete_room(db, room_id):
        raise HTTPException(status_code=404, detail="Room not found")

@router.post("/clear", status_code=204)
async def clear_rooms(db: AsyncSession = Depends(get_db)):
    await clear_all_rooms(db)
