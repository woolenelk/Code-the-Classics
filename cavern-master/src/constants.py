"""
constants.py — Shared constants, level data, helper functions, and the
               module-level singletons (current_game, _sounds).

Every other module imports from here rather than from game.py, which
keeps the dependency graph acyclic:

    constants  ←  base  ←  pop / bolt / orb / fruit / player / robot
                                         ↑
                                        game
"""

# ---------------------------------------------------------------------------
# Window / grid
# ---------------------------------------------------------------------------
WIDTH = 800
HEIGHT = 480

NUM_ROWS = 18
NUM_COLUMNS = 28

LEVEL_X_OFFSET = 50
GRID_BLOCK_SIZE = 25

# ---------------------------------------------------------------------------
# Anchor shortcuts
# ---------------------------------------------------------------------------
ANCHOR_CENTRE = ("center", "center")
ANCHOR_CENTRE_BOTTOM = ("center", "bottom")

# ---------------------------------------------------------------------------
# Robot type constants (used by both Robot and Fruit, defined here to
# avoid a Fruit → Robot import that would create a potential cycle)
# ---------------------------------------------------------------------------
ROBOT_TYPE_NORMAL = 0
ROBOT_TYPE_AGGRESSIVE = 1

# ---------------------------------------------------------------------------
# Level layouts
# ---------------------------------------------------------------------------
LEVELS = [
    [
        "XXXXX     XXXXXXXX     XXXXX",
        "", "", "", "",
        "   XXXXXXX        XXXXXXX   ",
        "", "", "",
        "   XXXXXXXXXXXXXXXXXXXXXX   ",
        "", "", "",
        "XXXXXXXXX          XXXXXXXXX",
        "", "", "",
    ],
    [
        "XXXX    XXXXXXXXXXXX    XXXX",
        "", "", "", "",
        "    XXXXXXXXXXXXXXXXXXXX    ",
        "", "", "",
        "XXXXXX                XXXXXX",
        "      X              X      ",
        "       X            X       ",
        "        X          X        ",
        "         X        X         ",
        "", "", "",
    ],
    [
        "XXXX    XXXX    XXXX    XXXX",
        "", "", "", "",
        "  XXXXXXXX        XXXXXXXX  ",
        "", "", "",
        "XXXX      XXXXXXXX      XXXX",
        "", "", "",
        "    XXXXXX        XXXXXX    ",
        "", "", "",
    ],
]

# ---------------------------------------------------------------------------
# Module-level singletons — set by Game.__init__ and main.py respectively
# ---------------------------------------------------------------------------
current_game = None   # type: "Game | None"
_sounds = None        # pgzero sounds object injected at startup


def set_current_game(g) -> None:
    global current_game
    current_game = g


def set_sounds(sounds_obj) -> None:
    global _sounds
    _sounds = sounds_obj


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sign(x: float) -> int:
    """Return -1 for negative numbers, +1 for zero or positive."""
    return -1 if x < 0 else 1


def block(x: int, y: int) -> bool:
    """Return True if there is a level grid block at pixel position (x, y)."""
    grid_x = (x - LEVEL_X_OFFSET) // GRID_BLOCK_SIZE
    grid_y = y // GRID_BLOCK_SIZE
    if 0 < grid_y < NUM_ROWS:
        row = current_game.grid[grid_y]
        return (
            grid_x >= 0
            and grid_x < NUM_COLUMNS
            and len(row) > 0
            and row[grid_x] != " "
        )
    return False