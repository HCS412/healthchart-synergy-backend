from fastapi import APIRouter

router = APIRouter()

@router.get("/rooms")
def get_rooms():
    # Eventually this will pull from your room logic / database
    return {
        "rooms": [
            {"id": "101", "status": "occupied", "fall_risk": True},
            {"id": "102", "status": "vacant", "fall_risk": False}
        ]
    }
