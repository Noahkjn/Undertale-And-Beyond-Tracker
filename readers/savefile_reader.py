"""
Parse Undertale's ``file0`` save file.

``file0`` is a plain-text file with one value per line (~549 lines).
Line numbers below are **1-based** (matching community documentation).

Confirmed layout (based on multiple community sources):
  1  – Player name
  2  – LV (LOVE)
  3  – Current HP
  4  – Max HP
  5  – AT (attack)
  6  – DF (defense)
  7  – Gold
  8  – EXP
  9  – Room ID
  10 – Playtime (seconds as a float/integer)
  11 – X position           (best-guess)
  12 – Y position           (best-guess)
  13-20 – Inventory item IDs (8 slots)
  21 – Equipped weapon ID   (best-guess)
  22 – Equipped armor ID    (best-guess)
  23 – Area kill count      (best-guess)
  24 – Total kill count     (best-guess)
  25 – Fun value (0-99)     (best-guess)
  26-65 – Box A items (up to 40 box slots total across boxes A–E)
  Lines 66+ contain various story/route flags.
"""
from __future__ import annotations

from typing import Any

from readers.lookups import (
    AREA_RANGES,
    get_area,
    get_item_name,
    get_room_name,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
INVENTORY_SIZE = 8          # lines 13-20  (indices 12-19)
BOX_SLOTS_PER_BOX = 8
BOX_COUNT = 5               # Box A through E
BOX_START_INDEX = 25        # line 26 (0-based index 25)  – best-guess

# Genocide kill-count thresholds per area (community-documented)
GENOCIDE_KILLS: dict[str, int] = {
    "Ruins":     20,
    "Snowdin":   16,
    "Waterfall": 18,
    "Hotland":   40,
    "Core":       8,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _int(value: str, default: int = 0) -> int:
    try:
        return int(float(value.strip()))
    except (ValueError, AttributeError):
        return default


def _float(value: str, default: float = 0.0) -> float:
    try:
        return float(value.strip())
    except (ValueError, AttributeError):
        return default


def _str(value: str) -> str:
    return value.strip()


def _format_playtime(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h}:{m:02d}:{s:02d}"


def _detect_route(total_kills: int, area_kills: int, room_id: int) -> str:
    """
    Rough route detection.
    - Genocide : total_kills above the sum of all area thresholds
    - Pacifist : zero total kills
    - Neutral  : everything else
    """
    if total_kills == 0:
        return "Pacifist"
    genocide_total = sum(GENOCIDE_KILLS.values())
    if total_kills >= genocide_total:
        return "Genocide"
    return "Neutral"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_file0(path: str) -> dict[str, Any]:
    """
    Parse *path* (the ``file0`` save file) and return a rich dictionary.

    On any read/parse error an empty dict is returned.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
    except OSError:
        return {}

    lines = raw.splitlines()

    def line(idx: int, default: str = "0") -> str:
        """Return line at 0-based *idx*, or *default* if out of range."""
        if 0 <= idx < len(lines):
            return lines[idx]
        return default

    # ── Core stats (lines 1-12 / indices 0-11) ────────────────────────────
    name      = _str(line(0, ""))           # line 1  – confirmed
    lv        = _int(line(1))               # line 2  – confirmed
    hp        = _int(line(2))               # line 3  – confirmed
    maxhp     = _int(line(3))               # line 4  – confirmed
    at        = _int(line(4))               # line 5  – best-guess
    df        = _int(line(5))               # line 6  – best-guess
    gold      = _int(line(6))               # line 7  – confirmed
    exp       = _int(line(7))               # line 8  – confirmed
    room_id   = _int(line(8))               # line 9  – confirmed
    playtime  = _int(line(9))               # line 10 – confirmed (seconds)
    x_pos     = _float(line(10))            # line 11 – best-guess
    y_pos     = _float(line(11))            # line 12 – best-guess

    # ── Inventory (lines 13-20 / indices 12-19) ───────────────────────────
    item_ids: list[int] = []
    for i in range(INVENTORY_SIZE):
        item_ids.append(_int(line(12 + i)))

    items = [get_item_name(iid) for iid in item_ids if iid != 0]
    item_ids_nonempty = [iid for iid in item_ids if iid != 0]

    # ── Equipment (lines 21-22 / indices 20-21) ───────────────────────────
    weapon_id = _int(line(20))              # line 21 – best-guess
    armor_id  = _int(line(21))              # line 22 – best-guess
    weapon    = get_item_name(weapon_id)
    armor     = get_item_name(armor_id)

    # ── Kill counts (lines 23-24 / indices 22-23) ─────────────────────────
    area_kills  = _int(line(22))            # line 23 – best-guess
    total_kills = _int(line(23))            # line 24 – best-guess

    # ── Fun value (line 25 / index 24) ────────────────────────────────────
    fun_value = _int(line(24))              # line 25 – best-guess
    # Clamp to valid range
    fun_value = max(0, min(99, fun_value))

    # ── Storage boxes (lines 26-65 / indices 25-64) ───────────────────────
    # Box A = indices 25-32, Box B = 33-40, Box C = 41-48, Box D = 49-56, Box E = 57-64
    boxes: list[list[str]] = []
    for box_num in range(BOX_COUNT):
        slot_start = BOX_START_INDEX + box_num * BOX_SLOTS_PER_BOX
        box_ids = [_int(line(slot_start + s)) for s in range(BOX_SLOTS_PER_BOX)]
        boxes.append([get_item_name(bid) for bid in box_ids if bid != 0])

    box_labels = ["box_a", "box_b", "box_c", "box_d", "box_e"]

    # ── Location / area ───────────────────────────────────────────────────
    location = get_room_name(room_id)
    area     = get_area(room_id)

    # ── Route detection ───────────────────────────────────────────────────
    route = _detect_route(total_kills, area_kills, room_id)

    # ── Playtime formatting ───────────────────────────────────────────────
    playtime_formatted = _format_playtime(playtime)

    # ── Remaining raw lines as flags (everything after index 64) ──────────
    # Collect up to 500 extra flag lines for completeness.
    flag_start = BOX_START_INDEX + BOX_COUNT * BOX_SLOTS_PER_BOX  # index 65
    flags: dict[str, str] = {}
    for i, raw_line in enumerate(lines[flag_start : flag_start + 500]):
        flags[f"flag_{flag_start + i + 1}"] = raw_line.strip()

    return {
        # Player stats
        "name":               name,
        "lv":                 lv,
        "hp":                 hp,
        "maxhp":              maxhp,
        "at":                 at,
        "df":                 df,
        "gold":               gold,
        "exp":                exp,
        # Position & room
        "room_id":            room_id,
        "location":           location,
        "area":               area,
        "x":                  x_pos,
        "y":                  y_pos,
        # Time
        "playtime":           playtime,
        "playtime_formatted": playtime_formatted,
        # Equipment
        "weapon":             weapon,
        "weapon_id":          weapon_id,
        "armor":              armor,
        "armor_id":           armor_id,
        # Inventory
        "items":              items,
        "item_ids":           item_ids_nonempty,
        "inventory_raw":      item_ids,
        # Kills & route
        "kills":              total_kills,
        "area_kills":         area_kills,
        "route":              route,
        # Fun value
        "fun_value":          fun_value,
        # Storage boxes
        **{box_labels[i]: boxes[i] for i in range(BOX_COUNT)},
        # All flags
        "flags":              flags,
        # Raw line dump for debugging
        "raw_lines":          lines,
    }
