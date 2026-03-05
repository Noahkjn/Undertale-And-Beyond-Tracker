# Undertale-And-Beyond-Tracker

Local web dashboard for tracking Undertale & Beyond stats in real time.  
Runs entirely on your machine — **no game modification required**.

---

## 🎮 How It Works

```
Undertale ──saves──► file0 + undertale.ini (on disk)
                               │
                               ▼
                     bridge.py  (watches for changes)
                               │
                               ▼  POST /api/update
                     Flask server (app.py :3000)
                               │
                               ▼  GET /api/state (polling)
                     Web Dashboard (browser)
```

`bridge.py` watches the files Undertale **already writes** when it saves.
No mods, no DLLs, no game files are modified.

---

## 🚀 Getting Started

### 1) Install Python
Install **Python 3.10+** from <https://www.python.org/downloads/>

### 2) Start the tracker server

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

### 5) Start the bridge (in a second terminal)

**Windows**
```bat
start_bridge.bat
```

**macOS / Linux**
```bash
chmod +x start_bridge.sh
./start_bridge.sh
```

The bridge auto-detects your Undertale save location.  
You can override it:

```bash
# Use a custom save directory
python bridge.py --save-dir "/path/to/saves"

# Attach to an existing session instead of creating a new one
python bridge.py --code ABC123

# Point at a remote server
python bridge.py --api-url http://192.168.1.5:3000

# Change how often saves are checked (default 0.5 s)
python bridge.py --interval 1.0
```

---

## 📊 Stats Tracked

| Field | Source |
|-------|--------|
| Name, LV, HP, Max HP | `file0` |
| AT, DF, Gold, EXP | `file0` |
| Weapon, Armor | `file0` |
| Location, Area, Room ID | `file0` |
| Route (Pacifist / Neutral / Genocide) | `file0` kill counts |
| Total kills, Area kills | `file0` |
| Playtime (formatted) | `file0` |
| Fun value (0–99) | `file0` |
| Inventory (8 slots) | `file0` |
| Storage boxes A–E | `file0` |
| Flowey flags, True Reset, Souls | `undertale.ini` |
| All character relationship flags | `undertale.ini` |

---

## 🗺️ Platform Support

| OS | Save directory |
|----|----------------|
| Windows | `%LOCALAPPDATA%\UNDERTALE\` |
| macOS | `~/Library/Application Support/com.tobyfox.undertale/` |
| Linux | `~/.config/UNDERTALE/` |

---

## 🔌 API Endpoints

- `POST /api/session/create` → create a session code
- `GET /api/state?code=ABC123` → read the latest payload
- `POST /api/update` → send payloads from the bridge

---

## 🛠️ Dependencies

- **Flask** — tracker web server
- **requests** — used by `bridge.py` to POST to the API

See `requirements.txt`.

---

## 📦 Project Structure

```
app.py               Flask server + SQLite storage
bridge.py            Save-file bridge (run separately)
readers/
  __init__.py
  lookups.py         Item / room / area lookup tables
  savefile_reader.py file0 parser
  ini_reader.py      undertale.ini parser
templates/           Dashboard HTML
static/              CSS + JS assets
requirements.txt
start.sh / start.bat          Start the server
start_bridge.sh / start_bridge.bat  Start the bridge
tracker.db           Local data store (created at runtime)
```
