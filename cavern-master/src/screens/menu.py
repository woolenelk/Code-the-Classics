"""
screens/menu.py — MenuScreen

Displays the title overlay while a playerless demo Game runs in the background.
Transitions to PlayScreen when SPACE is pressed.
"""

from src.game import Game


class MenuScreen:
    """Title / attract screen."""

    def __init__(self):
        # A playerless game runs in the background for the animated level
        self._bg_game = Game()

    def update(self, input_state, app):
        # Animate the background demo
        self._bg_game.update()

        if input_state.fire_pressed:
            # SPACE pressed — start a real game
            app.change_screen("play")

    def draw(self, screen):
        self._bg_game.draw(screen)

        # Title overlay
        screen.blit("title", (0, 0))

        # Animated "Press SPACE" prompt
        anim_frame = min(((self._bg_game.timer + 40) % 160) // 4, 9)
        screen.blit("space" + str(anim_frame), (130, 280))