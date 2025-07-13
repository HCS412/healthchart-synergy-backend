# 🏥 HealthChart Synergy Backend

**HealthChart Synergy** powers intelligent hospital room signage, patient flow orchestration, staff badge tracking, and real-time compliance monitoring.

Built with **FastAPI**, this backend serves as the foundation for modern hospital infrastructure, starting with a pilot MVP for a single floor (12–20 rooms).

---

## 🚀 Features

✅ Room status tracking  
✅ Staff badge-in/out tracking  
✅ Fall risk and isolation protocols  
✅ Real-time alert generation  
✅ Modular architecture, future EHR integrations  
✅ Live OpenAPI docs (`/docs`)

---

## 🧠 Modules Overview

| Module   | Description |
|----------|-------------|
| `rooms`  | Track room occupancy, fall risk, isolation, and patient info |
| `events` | Simulate EHR-style events like admit, discharge, transfer |
| `badges` | Simulate BLE/NFC badge-ins, track staff per room |
| `alerts` | Trigger alerts based on room + staff state (e.g., fall risk unattended) |

---

## 📁 Project Structure

app/
├── api/ # API route handlers
│ ├── rooms.py
│ ├── events.py
│ ├── badges.py
│ └── alerts.py
├── models/ # Pydantic schemas
│ ├── room.py
│ ├── event.py
│ ├── badge.py
│ └── alert.py
├── services/ # Business logic / state
│ ├── room_store.py
│ ├── badge_store.py
│ └── alert_logic.py
├── main.py # App entrypoint

yaml
Copy
Edit

---

## 🧪 Try It Live

Visit `/docs` to explore and test endpoints with FastAPI's built-in Swagger UI:


yaml
Copy
Edit

---

## 📦 Installation (Local or Cloud)

If cloning locally (optional):

```bash
git clone https://github.com/your-username/healthchart-synergy-backend.git
cd healthchart-synergy-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
🌐 Deployment
This project is deployed using Railway:

Connect Railway to GitHub

Add a Procfile:

less
Copy
Edit
web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
Push to GitHub — Railway auto-builds + deploys

✨ Future Roadmap
Integration with Epic EHR (ADT webhook support)

Postgres or Redis storage backend

Real-time signage updates via WebSocket or MQTT

BLE/NFC badge reader hardware integration

Frontend dashboard for command center

Admin login & audit logs

👨‍⚕️ Pilot Focus
This MVP targets a single hospital floor (12–20 rooms) and is optimized for:

High-fidelity prototype demonstrations

Safety-critical workflows (fall risk, isolation)

Extensible architecture for future modules

🤝 Contributing
Fork this repo

Use consistent code style (black, isort)

Submit a PR with clear description

📄 License
MIT © 2025 HealthChart Synergy

yaml
Copy
Edit

---

Let me know if you'd like:
- A version with badges (e.g. Railway status, Python version)
- To pin versions in `requirements.txt`
- A shorter version for LinkedIn or product page use

Ready to move forward to Phase 2?
