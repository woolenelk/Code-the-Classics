"""
entities/orb.py — Orb (player's projectile / enemy trap).

Orbs are fired by the Player, float upward after a brief horizontal
travel, and can trap Robots.  They pop when their timer expires or
when they are hit by a Bolt.
"""

from random import randint

import src.constants as _c
from src.entities.base import CollideActor
from src.entities.pop import Pop


class Orb(CollideActor):
    """A bubble orb fired by the Player."""

    MAX_TIMER = 250

    def __init__(self, pos, dir_x: int):
        super().__init__(pos)
        self.direction_x = dir_x
        self.floating = False
        self.trapped_enemy_type = None  # set when a Robot is caught
        self.timer = -1
        self.blown_frames = 6  # frames of horizontal travel before floating

    def hit_test(self, bolt) -> bool:
        """Called by Bolt.update — sets the orb close to expiry on hit."""
        collided = self.collidepoint(bolt.pos)
        if collided:
            self.timer = Orb.MAX_TIMER - 1
        return collided

    def update(self) -> None:
        # Import here to avoid a module-level circular reference
        # (Orb → Fruit → [nothing that imports Orb], but keeping the import
        # lazy makes the dependency obvious).
        from src.entities.fruit import Fruit

        g = _c.current_game
        self.timer += 1

        if self.floating:
            self.move(0, -1, randint(1, 2))
        else:
            if self.move(self.direction_x, 0, 4):
                self.floating = True

        if self.timer == self.blown_frames:
            self.floating = True
        elif self.timer >= Orb.MAX_TIMER or self.y <= -40:
            # Pop and optionally release a Fruit
            g.pops.append(Pop(self.pos, 1))
            if self.trapped_enemy_type is not None:
                g.fruits.append(Fruit(self.pos, self.trapped_enemy_type))
            g.play_sound("pop", 4)

        # Sprite selection
        if self.timer < 9:
            self.image = "orb" + str(self.timer // 3)
        else:
            if self.trapped_enemy_type is not None:
                self.image = (
                    "trap"
                    + str(self.trapped_enemy_type)
                    + str((self.timer // 4) % 8)
                )
            else:
                self.image = "orb" + str(3 + (((self.timer - 9) // 8) % 4))