from __future__ import annotations

import json
import os
import secrets
import sqlite3
import string
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

from flask import Flask, jsonify, redirect, render_template, request

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "tracker.db")

app = Flask(__name__)

@dataclass
class SessionState:
    code: str
    last_payload: Dict[str, Any]
    last_updated: Optional[int]

def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            code TEXT PRIMARY KEY,
            created_at INTEGER NOT NULL,
            last_updated INTEGER,
            last_payload TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_code TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            payload TEXT NOT NULL,
            FOREIGN KEY(session_code) REFERENCES sessions(code)
        )
        """
    )
    conn.commit()
    conn.close()

def generate_code(length: int = 6) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def create_session() -> str:
    conn = get_db()
    cur = conn.cursor()
    code = generate_code()
    created_at = int(time.time())
    cur.execute(
        "INSERT INTO sessions (code, created_at, last_updated, last_payload) VALUES (?, ?, NULL, NULL)",
        (code, created_at),
    )
    conn.commit()
    conn.close()
    return code

def get_session_state(code: str) -> Optional[SessionState]:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT code, last_updated, last_payload FROM sessions WHERE code = ?",
        (code,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    payload = {}
    if row["last_payload"]:
        payload = json.loads(row["last_payload"])
    return SessionState(code=row["code"], last_payload=payload, last_updated=row["last_updated"])

def update_session(code: str, payload: Dict[str, Any]) -> Optional[SessionState]:
    conn = get_db()
    cur = conn.cursor()
    now = int(time.time())
    payload_text = json.dumps(payload)
    cur.execute(
        "UPDATE sessions SET last_updated = ?, last_payload = ? WHERE code = ?",
        (now, payload_text, code),
    )
    if cur.rowcount == 0:
        conn.close()
        return None
    cur.execute(
        "INSERT INTO events (session_code, created_at, payload) VALUES (?, ?, ?)",
        (code, now, payload_text),
    )
    conn.commit()
    conn.close()
    return get_session_state(code)

@app.route("/")
def index() -> str:
    return render_template("index.html")

@app.route("/session/<code>")
def session_redirect(code: str):
    return redirect(f"/#/session/{code}")

@app.route("/api/session/create", methods=["POST"])
def api_session_create():
    code = create_session()
    join_url = f"/session/{code}"
    return jsonify({"code": code, "joinUrl": join_url})

@app.route("/api/state", methods=["GET"])
def api_state():
    code = request.args.get("code", "").strip().upper()
    if not code:
        return jsonify({"error": "Missing code"}), 400
    state = get_session_state(code)
    if not state:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(
        {
            "code": state.code,
            "lastUpdated": state.last_updated,
            "payload": state.last_payload,
        }
    )

@app.route("/api/update", methods=["POST"])
def api_update():
    data = request.get_json(silent=True) or {}
    code = str(data.get("code", "")).strip().upper()
    payload = data.get("payload", {})
    if not code:
        return jsonify({"error": "Missing code"}), 400
    if not isinstance(payload, dict):
        return jsonify({"error": "Payload must be an object"}), 400
    state = update_session(code, payload)
    if not state:
        return jsonify({"error": "Session not found"}), 404
    return jsonify({"ok": True, "lastUpdated": state.last_updated})

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=3000, debug=False)