# Undertale-And-Beyond-Tracker

Welcome to **Undertale-And-Beyond-Tracker**, the ultimate companion for tracking your gameplay stats in *Undertale* and related fan projects! This tracker is built with **Python** and provides a sleek **web interface** to monitor your in-game progress in real-time.  

---

## 🎮 Features

- **Real-Time Game Tracking**: Monitor your HP, LV, EXP, and other vital stats while playing.
- **Web-Based Dashboard**: View your stats in any browser via a local web app.
- **Easy Game Integration**: Connect your game to the tracker with a single click.
- **Cross-Platform Compatibility**: Works on Windows with Python installed.
- **Safe & Local**: All data stays on your machine — no external servers required.

---

## 🚀 Getting Started

Follow these steps to get your Undertale Tracker up and running:

### 1. Install Python
Make sure you have **Python 3.10+** installed on your PC. You can download it from the [official Python website](https://www.python.org/downloads/).

### 2. Launch the Tracker
Run the `start.bat` file included in the repository. This will:

- Install all required Python dependencies.
- Start the local web server that powers the tracker.

### 3. Open the Web App
Once the server is running, open your preferred web browser and navigate to:  

https://localhost:3000/


This is your dashboard where all tracked stats will appear.

### 4. Connect Your Game
1. Launch your Undertale (or compatible) game.
2. In the tracker menu, press the **Track** button.
3. Your game will attempt to send a connection request to the tracker server.
4. Accept the request in the web app to start receiving live stats.

### 5. Enjoy Tracking
Once connected, your stats should appear in real-time. Monitor your health, level, experience, and more while playing.

---

## 🛠️ Dependencies

The tracker uses Python and several key libraries:

- `Flask` – for running the web server
- `requests` – to handle HTTP connections between game and tracker
- `json` – to process game data
- Other dependencies listed in `requirements.txt`

You can install them manually using:

```bash
pip install -r requirements.txt
