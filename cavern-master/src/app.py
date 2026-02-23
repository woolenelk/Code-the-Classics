"""
app.py — App and screen management (State pattern).

App owns the currently active screen and is the single point of contact for
screen transitions.  Global update() and draw() in main.py delegate to it.
"""

from src.screens.menu import MenuScreen
from src.screens.play import PlayScreen
from src.screens.game_over import GameOverScreen


class App:
    """Top-level application object.  Owns the current screen."""

    def __init__(self):
        self._screen = MenuScreen()

    # ------------------------------------------------------------------
    # Public API called by global update() / draw()
    # ------------------------------------------------------------------

    def update(self, input_state):
        """Delegate per-frame logic to the active screen."""
        self._screen.update(input_state, self)

    def draw(self, screen):
        """Delegate rendering to the active screen."""
        self._screen.draw(screen)

    # ------------------------------------------------------------------
    # Screen transitions
    # ------------------------------------------------------------------

    def change_screen(self, name: str, **kwargs):
        """Switch to the named screen.

        Accepted names: ``"menu"``, ``"play"``, ``"game_over"``.
        Extra keyword arguments are forwarded to the screen constructor.
        """
        if name == "menu":
            self._screen = MenuScreen()
        elif name == "play":
            self._screen = PlayScreen()
        elif name == "game_over":
            self._screen = GameOverScreen(**kwargs)
        else:
            raise ValueError(f"Unknown screen name: {name!r}")