"""
screens/game_over.py — GameOverScreen

Shows the "Game Over" overlay.  Pressing SPACE returns to the menu.
"""

from src.game import Game

CHAR_WIDTH = [27, 26, 25, 26, 25, 25, 26, 25, 12, 26, 26, 25, 33, 25, 26,
              25, 27, 26, 26, 25, 26, 26, 38, 25, 25, 25]

WIDTH = 800
IMAGE_WIDTH = {"life": 44, "plus": 40, "health": 40}


def char_width(char):
    index = max(0, ord(char) - 65)
    return CHAR_WIDTH[index]


def draw_text(screen, text, y, x=None):
    if x is None:
        x = (WIDTH - sum(char_width(c) for c in text)) // 2
    for char in text:
        screen.blit("font0" + str(ord(char)), (x, y))
        x += char_width(char)


class GameOverScreen:
    """Displayed after the player loses all lives."""

    def __init__(self, score=0):
        # Keep a frozen game in the background
        self._bg_game = Game()
        self._score = score

    def update(self, input_state, app):
        self._bg_game.update()   # background animation keeps ticking

        if input_state.fire_pressed:
            app.change_screen("menu")

    def draw(self, screen):
        self._bg_game.draw(screen)
        self._draw_score(screen)
        screen.blit("over", (0, 0))

    def _draw_score(self, screen):
        number_width = CHAR_WIDTH[0]
        s = str(self._score)
        draw_text(screen, s, 451, WIDTH - 2 - (number_width * len(s)))
        draw_text(screen, "LEVEL 1", 451)