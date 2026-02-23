"""
main.py — Pygame Zero entry point.

This file is kept intentionally thin.  It:
  1. Declares the window constants Pygame Zero needs (WIDTH, HEIGHT, TITLE).
  2. Wires up the pgzero ``sounds`` object into src.game so entities can play audio.
  3. Creates the App singleton.
  4. Provides the global ``update()`` and ``draw()`` functions that Pygame Zero calls
     each frame — each is a single-line delegate to the App.

No game logic lives here.
"""

import sys
import pygame
import pgzero
import pgzrun

# ---------------------------------------------------------------------------
# Version guards (unchanged from original)
# ---------------------------------------------------------------------------
if sys.version_info < (3, 5):
    print("This game requires at least version 3.5 of Python. "
          "Please download it from www.python.org")
    sys.exit()

pgzero_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split(".")]
if pgzero_version < [1, 2]:
    print(
        f"This game requires at least version 1.2 of Pygame Zero. "
        f"You have version {pgzero.__version__}. "
        f"Please upgrade using: pip3 install --upgrade pgzero"
    )
    sys.exit()

# ---------------------------------------------------------------------------
# Window configuration (read by Pygame Zero before the game loop starts)
# ---------------------------------------------------------------------------
WIDTH = 800
HEIGHT = 480
TITLE = "Cavern"

# ---------------------------------------------------------------------------
# Boot the sound system
# ---------------------------------------------------------------------------
try:
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 1024)
    music.play("theme")
    music.set_volume(0.3)
except Exception:
    pass  # silently ignore audio failures

# ---------------------------------------------------------------------------
# Inject the pgzero sounds object into src.game so entities can play audio
# ---------------------------------------------------------------------------
import src.constants as _constants
_constants.set_sounds(sounds)   # ``sounds`` is injected by pgzrun into this namespace

# ---------------------------------------------------------------------------
# Create application and input handler
# ---------------------------------------------------------------------------
from src.app import App
from src.input import InputHandler

app = App()
_input_handler = InputHandler()

# ---------------------------------------------------------------------------
# Pygame Zero callbacks — thin delegates only
# ---------------------------------------------------------------------------

def update():
    input_state = _input_handler.snapshot(keyboard)
    app.update(input_state)


def draw():
    app.draw(screen)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
pgzrun.go()