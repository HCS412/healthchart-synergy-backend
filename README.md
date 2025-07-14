# 🏥 HealthChart Synergy Backend

**HealthChart Synergy** powers intelligent hospital room signage, patient flow orchestration, staff badge tracking, and real-time compliance monitoring.

Built with **FastAPI**, this backend serves as the foundation for modern hospital infrastructure, starting with a pilot MVP for a single floor (12–20 rooms).

---

## 🚀 Features

✅ Room status tracking  
✅ Staff badge-in/out tracking  
✅ Fall risk and isolation protocols  
✅ Real-time alert generation  
✅ JWT-based authentication with RBAC (nurse, admin, signage roles)  
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
| `auth`   | JWT authentication and RBAC for secure access |

---

## 📁 Project Structure

app/
├── api/ # API route handlers
│ ├── auth.py
│ ├── rooms.py
│ ├── events.py
│ ├── badges.py
│ ├── alerts.py
│ ├── signage.py
├── models/ # Pydantic schemas
│ ├── room.py
│ ├── event.py
│ ├── badge.py
│ ├── alert.py
│ ├── user.py
├── services/ # Business logic / state
│ ├── room_store.py
│ ├── badge_store.py
│ ├── event_handler.py
│ ├── fall_risk_alert.py
│ ├── isolation_alert.py
│ ├── alert_logic.py
├── auth.py
├── database.py
├── main.py

---

## 🧪 Try It Live

Visit `/docs` to explore and test endpoints with FastAPI's built-in Swagger UI. Use the `/login` endpoint to obtain a JWT for authenticated access.

**Default Users** (for testing):
- Admin: `username: admin, password: admin123` (full access)
- Nurse: `username: nurse, password: nurse123` (view rooms, badges, alerts)
- Signage: `username: signage, password: signage123` (view signage only)

---

## 📦 Installation (Local or Cloud)

If cloning locally (optional):

```bash
git clone https://github.com/your-username/healthchart-synergy-backend.git
cd healthchart-synergy-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

🌐 **Deployment**

This project is deployed using Railway:
- Connect Railway to GitHub
- Add a Procfile:
  ```
  web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
  ```
- Set environment variables in `.env`:
  ```
  DATABASE_URL=postgresql+asyncpg://postgres:password@postgres.railway.internal:5432/railway
  SECRET_KEY=your-secret-key-here
  ```
- Push to GitHub — Railway auto-builds + deploys

---

## ✨ Future Roadmap

- Integration with Epic EHR (ADT webhook support)
- Postgres or Redis storage backend
- Real-time signage updates via WebSocket or MQTT
- BLE/NFC badge reader hardware integration
- Frontend dashboard for command center
- Admin login & audit logs

---

## 👨‍⚕️ Pilot Focus

This MVP targets a single hospital floor (12–20 rooms) and is optimized for:
- High-fidelity prototype demonstrations
- Safety-critical workflows (fall risk, isolation)
- Extensible architecture for future modules

---

## 🤝 Contributing

- Fork this repo
- Use consistent code style (black, isort)
- Submit a PR with clear description

---

## 📄 License

MIT © 2025 HealthChart Synergy
