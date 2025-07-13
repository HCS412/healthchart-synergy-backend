from sqlalchemy.orm import Session
from app.models.room import Room, RoomDB
from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_all_rooms():
    with SessionLocal() as db:
        return db.query(RoomDB).all()

def get_room_by_id(room_id: str):
    with SessionLocal() as db:
        return db.query(RoomDB).filter(RoomDB.id == room_id).first()

def update_room(room: Room):
    with SessionLocal() as db:
        db_room = db.query(RoomDB).filter(RoomDB.id == room.id).first()
        if db_room:
            # Update existing
            db_room.status = room.status
            db_room.fall_risk = room.fall_risk
            db_room.isolation = room.isolation
            db_room.patient_name = room.patient_name
        else:
            # Create new
            db_room = RoomDB(**room.dict())
            db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room

def delete_room(room_id: str):
    with SessionLocal() as db:
        db_room = db.query(RoomDB).filter(RoomDB.id == room_id).first()
        if db_room:
            db.delete(db_room)
            db.commit()
            return True
        return False

def clear_all_rooms():
    with SessionLocal() as db:
        db.query(RoomDB).delete()
        db.commit()
