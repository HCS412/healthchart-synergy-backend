from fastapi import FastAPI
from app.api import rooms  # ⬅️ Import the router

app = FastAPI()

# Include the rooms API routes
app.include_router(rooms.router)

@app.get("/")
def read_root():
    return {"message": "HealthChart Synergy backend is live!"}
