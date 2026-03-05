"""
Lookup tables for Undertale save-file bridge.

Note: Item IDs and room IDs are based on community-documented values
(https://undertale.fandom.com) and may vary slightly between game
versions (v1.001, v1.08, Steam, Switch, etc.).  IDs marked with # ?
are best-guess estimates rather than confirmed values.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Item IDs → display names
# ---------------------------------------------------------------------------
# Consumables (0-46)
# Weapons (47-57)
# Armour  (58-64)
ITEM_NAMES: dict[int, str] = {
    0: "(Empty)",
    1: "Stick",
    2: "Bandage",
    3: "Monster Candy",
    4: "Croquet Roll",
    5: "Butterscotch Pie",
    6: "Spider Donut",
    7: "Snowman Piece",
    8: "Nice Cream",
    9: "Bisicle",
    10: "Unisicle",
    11: "Cinnamon Bunny",
    12: "Astronaut Food",
    13: "Instant Noodles",
    14: "Legendary Hero",
    15: "Glamburger",
    16: "Sea Tea",
    17: "Starfait",
    18: "Hush Puppy",
    19: "Temmie Flakes",
    20: "Dog Salad",
    21: "Dog Residue",
    22: "Steak in the Shape of Mettaton's Face",
    23: "Popato Chisps",
    24: "Junk Food",
    25: "Bad Memory",
    26: "Last Dream",
    27: "Nice Cream (almond)",          # ? alt flavour
    28: "Puppydough Icecream",
    29: "Bisicle (half)",               # ?
    30: "Hot Dog...?",
    31: "Hot Cat",
    32: "Punch Card",
    33: "Annoying Dog",
    34: "Spider Cider",
    35: "Tem Flake (premium)",          # ?
    36: "Face Steak",
    37: "Snail Pie",
    38: "Rock Candy",                   # ?
    39: "Pumpkin Rings",               # ?
    40: "Stoic Onion",                 # ?
    41: "Ghost Fruit",                 # ?
    42: "Crab Apple",                  # ?
    43: "Mystery Key",
    44: "Undyne's Letter",
    45: "Undyne's Letter EX",
    46: "Potato Chisps",               # ?
    # Weapons
    47: "Old Tutu",
    48: "Toy Knife",
    49: "Tough Glove",
    50: "Ballet Shoes",
    51: "Torn Notebook",
    52: "Burnt Pan",
    53: "Empty Gun",
    54: "Cowboy Hat",
    55: "Heart Locket",
    56: "The Real Knife",
    57: "The Locket",                  # ? (True Pacifist ending item)
    # Armour
    58: "Stained Apron",
    59: "Temmie Armor",
    60: "Faded Ribbon",
    61: "Manly Bandanna",
    62: "Old Tutu (armor)",            # ?
    63: "Cloudy Glasses",
    64: "Bandage (armor)",
}

# ---------------------------------------------------------------------------
# Weapon IDs (subset of ITEM_NAMES)
# ---------------------------------------------------------------------------
WEAPON_NAMES: dict[int, str] = {
    1: "Stick",
    47: "Old Tutu",
    48: "Toy Knife",
    49: "Tough Glove",
    50: "Ballet Shoes",
    51: "Torn Notebook",
    52: "Burnt Pan",
    53: "Empty Gun",
    54: "Cowboy Hat",
    55: "Heart Locket",
    56: "The Real Knife",
}

# ---------------------------------------------------------------------------
# Armour IDs (subset of ITEM_NAMES)
# ---------------------------------------------------------------------------
ARMOR_NAMES: dict[int, str] = {
    2: "Bandage",
    58: "Stained Apron",
    59: "Temmie Armor",
    60: "Faded Ribbon",
    61: "Manly Bandanna",
    62: "Old Tutu (armor)",
    63: "Cloudy Glasses",
    64: "Bandage (armor)",
}

# ---------------------------------------------------------------------------
# Area ranges: area name → (first_room_id, last_room_id)
# ---------------------------------------------------------------------------
AREA_RANGES: dict[str, tuple[int, int]] = {
    "Ruins":     (0,   44),
    "Snowdin":   (45,  102),
    "Waterfall": (103, 157),
    "Hotland":   (158, 194),
    "Core":      (195, 231),
    "New Home":  (232, 289),
}

# ---------------------------------------------------------------------------
# Room IDs → human-readable names
# Derived from community documentation; ? marks best-guess names.
# ---------------------------------------------------------------------------
ROOM_NAMES: dict[int, str] = {
    # ── Ruins (0-44) ───────────────────────────────────────────────────────
    0: "Intro / The Void",
    1: "Ruins – Entrance",
    2: "Ruins – Long Corridor",
    3: "Ruins – Leaf Pile Room",
    4: "Ruins – Rock Puzzle 1",
    5: "Ruins – Corridor",
    6: "Ruins – Flowey's Room",
    7: "Ruins – Toriel's Path",
    8: "Ruins – Puzzle Room",
    9: "Ruins – Froggo Room",
    10: "Ruins – Mice Hallway",
    11: "Ruins – Spider Bake Sale",
    12: "Ruins – Toriel's Home",
    13: "Ruins – Toriel's Kitchen",
    14: "Ruins – Toriel's Bedroom",
    15: "Ruins – Basement Corridor",
    16: "Ruins – Basement",
    17: "Ruins – Exit Door",
    18: "Ruins – Rock Puzzle 2",
    19: "Ruins – Spike Trap Room",
    20: "Ruins – Dummy Room",
    21: "Ruins – Transitional Hallway",
    22: "Ruins – Leaf Pile 2",
    23: "Ruins – Deeper Ruins",           # ?
    24: "Ruins – Corridor 2",             # ?
    25: "Ruins – Monster Room A",         # ?
    26: "Ruins – Monster Room B",         # ?
    27: "Ruins – Candy Dish",             # ?
    28: "Ruins – Large Chamber",          # ?
    29: "Ruins – Pillar Hall",            # ?
    30: "Ruins – Dark Hall",              # ?
    31: "Ruins – Checkerboard Room",      # ?
    32: "Ruins – Mossy Passage",          # ?
    33: "Ruins – Gate Hall",              # ?
    34: "Ruins – Lower Ruins",            # ?
    35: "Ruins – Staircase",              # ?
    36: "Ruins – Cavern",                 # ?
    37: "Ruins – Echo Flower Hall",       # ?
    38: "Ruins – Ruins Deeper",           # ?
    39: "Ruins – Transitional",           # ?
    40: "Ruins – Pre-Boss",               # ?
    41: "Ruins – Boss Room",              # ?
    42: "Ruins – After Boss",             # ?
    43: "Ruins – Exit Passage",           # ?
    44: "Ruins – Exit to Snowdin",

    # ── Snowdin (45-102) ───────────────────────────────────────────────────
    45: "Snowdin – Entry Forest",
    46: "Snowdin – Forest Path",
    47: "Snowdin – Sentry Station",
    48: "Snowdin – Piano Puzzle",
    49: "Snowdin – Dogi's House",         # ?
    50: "Snowdin – Ice Puzzle",
    51: "Snowdin – Frozen Pond",
    52: "Snowdin – Snowdin Town",
    53: "Snowdin – Inn",
    54: "Snowdin – Library",
    55: "Snowdin – Papyrus's House",
    56: "Snowdin – Sans's Room",
    57: "Snowdin – Grillby's",
    58: "Snowdin – Shop",
    59: "Snowdin – Forest 2",             # ?
    60: "Snowdin – Gauntlet of Deadly Terror",
    61: "Snowdin – Greater Dog Room",     # ?
    62: "Snowdin – Box Road",             # ?
    63: "Snowdin – Icicle Path",          # ?
    64: "Snowdin – Bridge Seed Puzzle",   # ?
    65: "Snowdin – Corridor",             # ?
    66: "Snowdin – Pre-Papyrus",          # ?
    67: "Snowdin – Papyrus Battle",
    68: "Snowdin – After Papyrus",        # ?
    69: "Snowdin – Forest Deep",          # ?
    70: "Snowdin – Hidden Area",          # ?
    71: "Snowdin – Dogamy & Dogaressa",   # ?
    72: "Snowdin – Dog Date",             # ?
    73: "Snowdin – Ice Cap Area",         # ?
    74: "Snowdin – Snowman",
    75: "Snowdin – Waterfall Entry",      # ?
    76: "Snowdin – Corridor 3",           # ?
    77: "Snowdin – Forest 3",             # ?
    78: "Snowdin – Transition",           # ?
    79: "Snowdin – Deeper Forest",        # ?
    80: "Snowdin – Slide",                # ?
    81: "Snowdin – Snowdrake Room",       # ?
    82: "Snowdin – Ice Field",            # ?
    83: "Snowdin – Frozen Lake",          # ?
    84: "Snowdin – Corridor 4",           # ?
    85: "Snowdin – Sans Telescope",       # ?
    86: "Snowdin – Snowy Path",           # ?
    87: "Snowdin – Inner Forest",         # ?
    88: "Snowdin – Hallway",              # ?
    89: "Snowdin – Shortcut",             # ?
    90: "Snowdin – Long Path",            # ?
    91: "Snowdin – Winding Path",         # ?
    92: "Snowdin – End Forest",           # ?
    93: "Snowdin – Last Stretch",         # ?
    94: "Snowdin – Pre-Forest Boss",      # ?
    95: "Snowdin – Forest Boss",          # ?
    96: "Snowdin – Forest Exit",          # ?
    97: "Snowdin – Upper Snowdin",        # ?
    98: "Snowdin – Alley",                # ?
    99: "Snowdin – Near River",           # ?
    100: "Snowdin – Transition Path",     # ?
    101: "Snowdin – Edge",                # ?
    102: "Snowdin – Exit to Waterfall",

    # ── Waterfall (103-157) ────────────────────────────────────────────────
    103: "Waterfall – Entrance",
    104: "Waterfall – Crystal Corridor",
    105: "Waterfall – Quiet Water",
    106: "Waterfall – Umbrella Room",
    107: "Waterfall – Dock",
    108: "Waterfall – Wishing Room",
    109: "Waterfall – Sans's Sentry Post",
    110: "Waterfall – Temmie Village",
    111: "Waterfall – Temmie Shop",
    112: "Waterfall – Mushroom Room",
    113: "Waterfall – Mad Dummy Room",    # ?
    114: "Waterfall – Crystal Cave",
    115: "Waterfall – Arrow Puzzle",
    116: "Waterfall – Undyne Chase",
    117: "Waterfall – Undyne Spear Field",
    118: "Waterfall – Memory Hall",
    119: "Waterfall – Echo Flower Path",
    120: "Waterfall – Deeper Waterfall",
    121: "Waterfall – Onionsan Lake",
    122: "Waterfall – Hollow Bridge",
    123: "Waterfall – Glow Worm Cave",
    124: "Waterfall – Monster Kid Bridge",
    125: "Waterfall – Napstablook's",
    126: "Waterfall – Dancefloor",        # ?
    127: "Waterfall – Piano Bridge",
    128: "Waterfall – Quiet Alcove",      # ?
    129: "Waterfall – Crystal Hall",      # ?
    130: "Waterfall – Lantern Path",      # ?
    131: "Waterfall – Rain Room",         # ?
    132: "Waterfall – Wishing Alcove",    # ?
    133: "Waterfall – Stone Bridge",      # ?
    134: "Waterfall – Mid-Waterfall",     # ?
    135: "Waterfall – Deep Pool",         # ?
    136: "Waterfall – Fog Room",          # ?
    137: "Waterfall – Lily Pad Room",     # ?
    138: "Waterfall – Deeper Cave",       # ?
    139: "Waterfall – Undyne House",
    140: "Waterfall – Undyne Exterior",   # ?
    141: "Waterfall – Final Chase",       # ?
    142: "Waterfall – Bridge to Hotland",
    143: "Waterfall – Crystal Path 2",    # ?
    144: "Waterfall – Corridor",          # ?
    145: "Waterfall – Upper Path",        # ?
    146: "Waterfall – Mushroom Field",    # ?
    147: "Waterfall – Cave Path",         # ?
    148: "Waterfall – Lower Path",        # ?
    149: "Waterfall – River Person",      # ?
    150: "Waterfall – Hidden Room",       # ?
    151: "Waterfall – Path East",         # ?
    152: "Waterfall – Path West",         # ?
    153: "Waterfall – Long Corridor",     # ?
    154: "Waterfall – Junction",          # ?
    155: "Waterfall – Pre-Undyne",        # ?
    156: "Waterfall – Undyne Battle",
    157: "Waterfall – Exit to Hotland",

    # ── Hotland (158-194) ──────────────────────────────────────────────────
    158: "Hotland – Entrance",
    159: "Hotland – Alphys's Lab",
    160: "Hotland – Lab Corridor",
    161: "Hotland – Conveyor Belts 1",
    162: "Hotland – Conveyor Belts 2",
    163: "Hotland – Laser Grid",
    164: "Hotland – Spider Room",         # ? (Muffet's area)
    165: "Hotland – Muffet's Bakery",
    166: "Hotland – MTT Resort",
    167: "Hotland – MTT Restaurant",
    168: "Hotland – Elevator R1",
    169: "Hotland – Elevator R2",
    170: "Hotland – Lava Crossing",
    171: "Hotland – News Stand",
    172: "Hotland – Quiz Show",
    173: "Hotland – Hotel Room",          # ?
    174: "Hotland – Hotel Roof",          # ?
    175: "Hotland – River Person",        # ?
    176: "Hotland – Deeper Hotland",      # ?
    177: "Hotland – Cooking Show",        # ?
    178: "Hotland – Hall of Progress",    # ?
    179: "Hotland – Inner Lab",           # ?
    180: "Hotland – True Lab Entrance",   # ?
    181: "Hotland – True Lab Hallway",    # ?
    182: "Hotland – True Lab Power Room", # ?
    183: "Hotland – True Lab Save",       # ?
    184: "Hotland – Conveyor 3",          # ?
    185: "Hotland – Lava Bridge 1",       # ?
    186: "Hotland – Lava Bridge 2",       # ?
    187: "Hotland – Catwalk",             # ?
    188: "Hotland – Waterfall Elevator",  # ?
    189: "Hotland – Pre-MTT",             # ?
    190: "Hotland – MTT Music Hall",      # ?
    191: "Hotland – Cooking Show Stage",  # ?
    192: "Hotland – Main Stage",          # ?
    193: "Hotland – Dressing Room",       # ?
    194: "Hotland – Exit to Core",

    # ── Core (195-231) ─────────────────────────────────────────────────────
    195: "Core – Entrance",
    196: "Core – Switch Puzzle",
    197: "Core – East Path",
    198: "Core – West Path",
    199: "Core – Junction",
    200: "Core – Mettaton Boss Room",
    201: "Core – After Mettaton",
    202: "Core – Long Corridor",
    203: "Core – Power Room",             # ?
    204: "Core – Last Corridor",          # ?
    205: "Core – Near Exit",              # ?
    206: "Core – Generator Room",         # ?
    207: "Core – Inner Core",             # ?
    208: "Core – Maintenance",            # ?
    209: "Core – Catwalk",                # ?
    210: "Core – Deeper Core",            # ?
    211: "Core – Puzzle 2",               # ?
    212: "Core – Puzzle 3",               # ?
    213: "Core – Elevator Area",          # ?
    214: "Core – Lava Room",              # ?
    215: "Core – Control Room",           # ?
    216: "Core – Final Stretch",          # ?
    217: "Core – Exit Corridor",          # ?
    218: "Core – Pre-Judgment",           # ?
    219: "Core – Judgment Approach",      # ?
    220: "Core – Hallway",                # ?
    221: "Core – Upper Core",             # ?
    222: "Core – Switch Hall",            # ?
    223: "Core – Blocked Path",           # ?
    224: "Core – Maintenance Shaft",      # ?
    225: "Core – Bypass",                 # ?
    226: "Core – Loading Bay",            # ?
    227: "Core – Hidden Room",            # ?
    228: "Core – Inner Sanctum",          # ?
    229: "Core – Last Room",              # ?
    230: "Core – Exit Hall",              # ?
    231: "Core – Exit to New Home",

    # ── New Home / Endgame (232-289+) ──────────────────────────────────────
    232: "New Home – Entry Hall",
    233: "New Home – Corridor",
    234: "New Home – Living Room",
    235: "New Home – Kitchen",
    236: "New Home – Asgore's Room",
    237: "New Home – Basement",
    238: "New Home – Hallway of Memories",
    239: "New Home – Long Corridor",
    240: "New Home – Judgement Hall",
    241: "New Home – Asgore's Garden",
    242: "New Home – Asgore Battle",
    243: "New Home – Barrier Room",
    244: "New Home – Beyond the Barrier",
    245: "New Home – Flowey Omega Fight",
    246: "New Home – True End",           # ?
    247: "New Home – Credits",            # ?
    248: "New Home – Post-Credits",       # ?
    249: "New Home – True Lab Room 1",    # ?
    250: "New Home – True Lab Room 2",    # ?
    251: "New Home – True Lab Room 3",    # ?
    252: "New Home – True Lab Room 4",    # ?
    253: "New Home – True Lab Room 5",    # ?
    254: "New Home – True Lab Monster A", # ?
    255: "New Home – True Lab Monster B", # ?
    256: "New Home – True Lab Monster C", # ?
    257: "New Home – True Lab Monster D", # ?
    258: "New Home – True Lab Exit",      # ?
    259: "New Home – Amalgamate Hall",    # ?
    260: "New Home – Final Save",         # ?
    261: "New Home – Asriel Battle 1",    # ?
    262: "New Home – Asriel Battle 2",    # ?
    263: "New Home – Asriel Battle 3",    # ?
    264: "New Home – Ending A",           # ?
    265: "New Home – Ending B",           # ?
    266: "New Home – Ending C",           # ?
    267: "New Home – Ending D",           # ?
    268: "New Home – Ending E",           # ?
    269: "New Home – Memory Hall 2",      # ?
    270: "New Home – Pacifist Reveal",    # ?
    271: "New Home – True End Corridor",  # ?
    272: "New Home – Pacifist Credits",   # ?
    273: "New Home – Post-Pacifist",      # ?
    274: "New Home – Black Room",         # ?
    275: "New Home – Gaster Room",        # ?
    276: "New Home – W. D. Gaster",       # ?
    277: "New Home – Hidden",             # ?
    278: "New Home – Void",               # ?
    279: "New Home – Locket Room",        # ?
    280: "New Home – Genocide End",       # ?
    281: "New Home – Post-Genocide",      # ?
    282: "New Home – Inner Room",         # ?
    283: "New Home – Deep End",           # ?
    284: "New Home – Finale",             # ?
    285: "New Home – After Story",        # ?
    286: "New Home – Void 2",             # ?
    287: "New Home – Unknown Room",       # ?
    288: "New Home – Unknown Room 2",     # ?
    289: "New Home – Unknown Room 3",     # ?
}


def get_room_name(room_id: int) -> str:
    """Return the best-known name for *room_id*, falling back to an area label."""
    if room_id in ROOM_NAMES:
        return ROOM_NAMES[room_id]
    for area, (start, end) in AREA_RANGES.items():
        if start <= room_id <= end:
            return f"{area} (room {room_id})"
    return f"Unknown (room {room_id})"


def get_area(room_id: int) -> str:
    """Return the area name for *room_id*."""
    for area, (start, end) in AREA_RANGES.items():
        if start <= room_id <= end:
            return area
    return "Unknown"


def get_item_name(item_id: int) -> str:
    """Return the item name for *item_id*, falling back to a numbered placeholder."""
    return ITEM_NAMES.get(item_id, f"Item #{item_id}")
