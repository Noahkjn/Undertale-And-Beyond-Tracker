# Undertale-And-Beyond-Tracker

Local web dashboard for tracking Undertale & Beyond stats in real time. Runs entirely on your machine.

---

## 🎮 Features

- **Real-time stats**: HP, LV, EXP, Gold, Location, Items.
- **Session codes**: Create a session and share a join link.
- **Local-only**: SQLite storage in `tracker.db`.
- **Simple setup**: One script to install deps and run.

---

## 🚀 Getting Started

### 1) Install Python
Install **Python 3.10+** from https://www.python.org/downloads/

### 2) Start the tracker

**Windows**
```bat
start.bat
```

**macOS / Linux**
```bash
chmod +x start.sh
./start.sh
```

### 3) Open the dashboard
Navigate to:
```
http://127.0.0.1:3000/
```

### 4) Create or connect a session
- Click **Create Session** to generate a code and join link.
- Or enter an existing code and click **Connect**.

---

## 🔌 API Endpoints

- `POST /api/session/create` → create a session code
- `GET /api/state?code=ABC123` → read the latest payload
- `POST /api/update` → send payloads from the game

Example payload:
```json
{
  "code": "ABC123",
  "payload": {
    "hp": 20,
    "lv": 3,
    "exp": 120,
    "gold": 55,
    "location": "Ruins",
    "items": ["Stick", "Bandage"]
  }
}
```

---

## 🛠️ Dependencies

- Flask (see `requirements.txt`)

---

## 📦 Project Structure

- `app.py` — Flask server + SQLite storage
- `templates/` — Dashboard HTML
- `static/` — CSS/JS assets
- `tracker.db` — Local data store (created at runtime)