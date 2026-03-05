#!/usr/bin/env python3
"""
bridge.py – Undertale save-file bridge
=======================================
Watches ``file0`` and ``undertale.ini`` for changes, parses them, and
POSTs the extracted data to the Flask tracker API at ``POST /api/update``.

No game modification is required – this script only reads files that
Undertale writes automatically when it saves.

Usage
-----
    python bridge.py [--save-dir PATH] [--code CODE] [--api-url URL]
                     [--interval SECONDS]

Options
    --save-dir  Path to the directory containing file0 and undertale.ini.
                Defaults to the platform-appropriate location.
    --code      Session code to use.  A new session is created when omitted.
    --api-url   Base URL of the Flask tracker (default: http://127.0.0.1:3000).
    --interval  Polling interval in seconds (default: 0.5).
"""
from __future__ import annotations

import argparse
import os
import platform
import sys
import time
from typing import Any

try:
    import requests
except ImportError:
    sys.exit(
        "The 'requests' library is required.\n"
        "Install it with:  pip install requests"
    )

from readers.ini_reader import parse_ini
from readers.savefile_reader import parse_file0

# ---------------------------------------------------------------------------
# Save-directory detection
# ---------------------------------------------------------------------------

def default_save_dir() -> str:
    """Return the default Undertale save directory for the current OS."""
    system = platform.system()
    if system == "Windows":
        appdata = os.environ.get("LOCALAPPDATA", "")
        return os.path.join(appdata, "UNDERTALE")
    if system == "Darwin":
        return os.path.expanduser(
            "~/Library/Application Support/com.tobyfox.undertale"
        )
    # Linux / other
    return os.path.expanduser("~/.config/UNDERTALE")


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def create_session(api_url: str) -> str:
    """Create a new tracker session and return its code."""
    url = f"{api_url}/api/session/create"
    resp = requests.post(url, timeout=10)
    resp.raise_for_status()
    code: str = resp.json()["code"]
    return code


def post_update(api_url: str, code: str, payload: dict[str, Any]) -> bool:
    """POST *payload* to the tracker API.  Returns True on success."""
    url = f"{api_url}/api/update"
    body = {"code": code, "payload": payload}
    try:
        resp = requests.post(url, json=body, timeout=10)
        resp.raise_for_status()
        return True
    except requests.RequestException as exc:
        print(f"  [!] POST failed: {exc}")
        return False


# ---------------------------------------------------------------------------
# File watching helpers
# ---------------------------------------------------------------------------

def mtime(path: str) -> float:
    """Return mtime of *path*, or 0 if it does not exist."""
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


def build_payload(
    save_dir: str,
    file0_path: str,
    ini_path: str,
) -> dict[str, Any]:
    """Parse both save files and merge into a single payload dict."""
    payload: dict[str, Any] = {}

    # Parse file0
    if os.path.isfile(file0_path):
        parsed = parse_file0(file0_path)
        payload.update(parsed)
    else:
        print("  [~] file0 not found – game may not have saved yet")

    # Parse undertale.ini
    if os.path.isfile(ini_path):
        ini_data = parse_ini(ini_path)
        payload["ini_data"] = ini_data

        # Surface commonly used INI values at the top level for convenience
        general = ini_data.get("general", {})
        if "name" in general and not payload.get("name"):
            payload["name"] = general["name"]
        if "love" in general and not payload.get("lv"):
            try:
                payload["lv"] = int(general["love"])
            except ValueError:
                pass

        flowey = ini_data.get("flowey", {})
        if flowey:
            payload["flowey_met"]          = flowey.get("Met", "0")
            payload["flowey_omega_fight"]  = flowey.get("FloweyOmegaFight", "0")

        reset_data = ini_data.get("reset", {})
        if reset_data:
            payload["true_reset"]  = reset_data.get("TrueReset", "0")
            payload["genocide_run"] = reset_data.get("Genocide", "0")
            payload["souls"]       = reset_data.get("Souls", "0")

        fun_section = ini_data.get("fffff", {})
        if fun_section and "fun_value" not in payload:
            try:
                payload["fun_value"] = int(fun_section.get("F", 0))
            except ValueError:
                pass
    else:
        print("  [~] undertale.ini not found – skipping INI data")

    return payload


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run(
    save_dir: str,
    code: str,
    api_url: str,
    interval: float,
) -> None:
    file0_path = os.path.join(save_dir, "file0")
    ini_path   = os.path.join(save_dir, "undertale.ini")

    print(f"[i] Session code : {code}")
    print(f"[i] API URL      : {api_url}")
    print(f"[i] Save dir     : {save_dir}")
    print(f"[i] Watching     : {file0_path}")
    print(f"[i]              : {ini_path}")
    print(f"[i] Poll interval: {interval}s")
    print("[*] Watching for save changes – press Ctrl+C to stop.\n")

    last_mtime_file0 = 0.0
    last_mtime_ini   = 0.0

    try:
        while True:
            try:
                mt_file0 = mtime(file0_path)
                mt_ini   = mtime(ini_path)

                if mt_file0 != last_mtime_file0 or mt_ini != last_mtime_ini:
                    ts = time.strftime("%H:%M:%S")
                    print(f"[{ts}] Save change detected – parsing …")

                    payload = build_payload(save_dir, file0_path, ini_path)

                    if payload:
                        ok = post_update(api_url, code, payload)
                        if ok:
                            name  = payload.get("name", "?")
                            hp    = payload.get("hp", "?")
                            maxhp = payload.get("maxhp", "?")
                            lv    = payload.get("lv", "?")
                            loc   = payload.get("location", "?")
                            print(
                                f"[{ts}] Posted – {name}  "
                                f"HP {hp}/{maxhp}  LV {lv}  @ {loc}"
                            )
                        else:
                            print(f"[{ts}] Failed to post update.")
                    else:
                        print(f"[{ts}] No data extracted (save may be empty).")

                    last_mtime_file0 = mt_file0
                    last_mtime_ini   = mt_ini

                time.sleep(interval)

            except (OSError, ValueError, requests.RequestException) as exc:
                print(f"[!] Error: {exc}")
                time.sleep(interval)
            except Exception as exc:  # noqa: BLE001 – unexpected errors should not crash the watch loop
                import traceback
                print(f"[!] Unexpected error: {exc}")
                traceback.print_exc()
                time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[*] Stopped.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Undertale save-file bridge – watch saves and POST to tracker API",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--save-dir",
        default=None,
        help="Path to the Undertale save directory (auto-detected by OS if omitted)",
    )
    parser.add_argument(
        "--code",
        default=None,
        help="Tracker session code (a new session is created when omitted)",
    )
    parser.add_argument(
        "--api-url",
        default="http://127.0.0.1:3000",
        help="Base URL of the Flask tracker API",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
        help="Polling interval in seconds",
    )
    args = parser.parse_args()

    save_dir = args.save_dir or default_save_dir()
    api_url  = args.api_url.rstrip("/")

    # Verify (or create) session
    code = args.code
    if code:
        code = code.strip().upper()
        print(f"[*] Using provided session code: {code}")
    else:
        print("[*] No session code provided – creating a new session …")
        try:
            code = create_session(api_url)
            print(f"[*] New session created: {code}")
            print(f"[*] Dashboard: {api_url}/session/{code}")
        except (requests.RequestException, OSError, KeyError, ValueError) as exc:
            sys.exit(f"[!] Could not create session: {exc}")

    run(save_dir=save_dir, code=code, api_url=api_url, interval=args.interval)


if __name__ == "__main__":
    main()
