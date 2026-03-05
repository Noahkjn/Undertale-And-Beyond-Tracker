"""
Parse Undertale's ``undertale.ini`` companion save file.

``undertale.ini`` uses standard INI format and is read with Python's
built-in ``configparser``.  All sections and keys are extracted and
returned as a nested dict ``{section_lower: {key: value}}``.

Known sections (may not all be present in every save):
  [General]  – Name, Love, HP, Room, …
  [Reset]    – TrueReset, Genocide, Souls, …
  [Flowey]   – Met, Kills, FloweyOmegaFight, …
  [FFFFF]    – F (fun value)
  [Toriel], [Sans], [Papyrus], [Undyne], [Alphys], [MTT], [Asgore]
             – character-specific friendship/date/kill flags
"""
from __future__ import annotations

import configparser
from typing import Any


def parse_ini(path: str) -> dict[str, Any]:
    """
    Parse *path* (``undertale.ini``) and return a nested dict.

    ``{ "general": { "Name": "FRISK", … }, "flowey": { "Met": "1", … }, … }``

    On any read/parse error an empty dict is returned.
    """
    parser = configparser.RawConfigParser()
    parser.optionxform = str  # preserve original key capitalisation

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
    except OSError:
        return {}

    try:
        parser.read_string(raw)
    except configparser.Error:
        return {}

    result: dict[str, dict[str, str]] = {}
    for section in parser.sections():
        result[section.lower()] = dict(parser.items(section))

    return result
