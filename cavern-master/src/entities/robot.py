"""
entities/robot.py — Robot (enemy).

Robots patrol the level, fire Bolts at the Player, and can be trapped
in Orbs.  Two types exist: TYPE_NORMAL and TYPE_AGGRESSIVE.
"""

from random import choice, randint, random

import src.constants as _c
from src.constants import (
    ROBOT_TYPE_AGGRESSIVE,
    ROBOT_TYPE_NORMAL,
    sign,
)
from src.entities.base import GravityActor
from src.entities.bolt import Bolt


class Robot(GravityActor):
    """An enemy that patrols and fires bolts at the player."""

    # Mirror constants.py values as class attributes for external readability
    TYPE_NORMAL = ROBOT_TYPE_NORMAL
    TYPE_AGGRESSIVE = ROBOT_TYPE_AGGRESSIVE

    def __init__(self, pos, type_: int):
        super().__init__(pos)
        self.type = type_
        self.speed = randint(1, 3)
        self.direction_x = 1
        self.alive = True
        self.change_dir_timer = 0
        self.fire_timer = 100

    def update(self) -> None:
        g = _c.current_game
        super().update()

        self.change_dir_timer -= 1
        self.fire_timer += 1

        # Move horizontally; reverse on wall collision
        if self.move(self.direction_x, 0, self.speed):
            self.change_dir_timer = 0

        # Periodically choose a new direction (biased toward the player)
        if self.change_dir_timer <= 0:
            directions = [-1, 1]
            if g.player:
                directions.append(sign(g.player.x - self.x))
            self.direction_x = choice(directions)
            self.change_dir_timer = randint(100, 250)

        # Aggressive robots deliberately aim at nearby orbs
        if self.type == Robot.TYPE_AGGRESSIVE and self.fire_timer >= 24:
            for orb in g.orbs:
                if (
                    orb.y >= self.top
                    and orb.y < self.bottom
                    and abs(orb.x - self.x) < 200
                ):
                    self.direction_x = sign(orb.x - self.x)
                    self.fire_timer = 0
                    break

        # Fire at the player — more likely when at the same height
        if self.fire_timer >= 12:
            fire_probability = g.fire_probability()
            if g.player and self.top < g.player.bottom and self.bottom > g.player.top:
                fire_probability *= 10
            if random() < fire_probability:
                self.fire_timer = 0
                g.play_sound("laser", 4)

        elif self.fire_timer == 8:
            # Frame 8 of the fire animation is when the bolt is actually launched
            g.bolts.append(
                Bolt((self.x + self.direction_x * 20, self.y - 38), self.direction_x)
            )

        # Check for capture by an orb
        for orb in g.orbs:
            if orb.trapped_enemy_type is None and self.collidepoint(orb.center):
                self.alive = False
                orb.floating = True
                orb.trapped_enemy_type = self.type
                g.play_sound("trap", 4)
                break

        # --- Sprite selection ---
        direction_idx = "1" if self.direction_x > 0 else "0"
        image = "robot" + str(self.type) + direction_idx
        if self.fire_timer < 12:
            image += str(5 + (self.fire_timer // 4))
        else:
            image += str(1 + ((g.timer // 4) % 4))
        self.image = image