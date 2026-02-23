"""
screens/play.py — PlayScreen

Active gameplay screen.  Handles pause (P key) and detects game-over.
"""

from src.game import Game
from src.entities.player import Player

# Character widths and drawing helpers live here too (originally in cavern.py)
CHAR_WIDTH = [27, 26, 25, 26, 25, 25, 26, 25, 12, 26, 26, 25, 33, 25, 26,
              25, 27, 26, 26, 25, 26, 26, 38, 25, 25, 25]

WIDTH = 800
HEIGHT = 480

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


def draw_status(screen, player):
    number_width = CHAR_WIDTH[0]
    s = str(player.score)
    draw_text(screen, s, 451, WIDTH - 2 - (number_width * len(s)))

    draw_text(screen, "LEVEL " + str(player._level_ref + 1), 451)

    lives_health = ["life"] * min(2, player.lives)
    if player.lives > 2:
        lives_health.append("plus")
    if player.lives >= 0:
        lives_health += ["health"] * player.health

    x = 0
    for image in lives_health:
        screen.blit(image, (x, 450))
        x += IMAGE_WIDTH[image]


class PlayScreen:
    """Active gameplay with optional pause."""

    def __init__(self):
        player = Player()
        self.game = Game(player)
        self._paused = False

    def update(self, input_state, app):
        # Toggle pause (P edge)
        if input_state.pause_pressed:
            self._paused = not self._paused

        if self._paused:
            return  # simulation frozen

        # Check for game over before updating
        if self.game.player.lives < 0:
            self.game.play_sound("over")
            app.change_screen("game_over", score=self.game.player.score)
            return

        self.game.update(input_state)

    def draw(self, screen):
        self.game.draw(screen)
        self._draw_status(screen)

        if self._paused:
            # Semi-transparent pause banner
            self._draw_pause_overlay(screen)

    # ------------------------------------------------------------------
    def _draw_status(self, screen):
        player = self.game.player
        number_width = CHAR_WIDTH[0]
        s = str(player.score)
        draw_text(screen, s, 451, WIDTH - 2 - (number_width * len(s)))

        draw_text(screen, "LEVEL " + str(self.game.level + 1), 451)

        lives_health = ["life"] * min(2, player.lives)
        if player.lives > 2:
            lives_health.append("plus")
        if player.lives >= 0:
            lives_health += ["health"] * player.health

        x = 0
        for image in lives_health:
            screen.blit(image, (x, 450))
            x += IMAGE_WIDTH[image]

    def _draw_pause_overlay(self, screen):
        # Dark semi-transparent rectangle across the centre
        import pygame
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.surface.blit(overlay, (0, 0))
        draw_text(screen, "PAUSED", HEIGHT // 2 - 20)