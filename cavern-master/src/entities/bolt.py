"""
entities/bolt.py — Bolt (enemy projectile).

Bolts are fired horizontally by Robots and destroy themselves on
hitting a block, an Orb, or the Player.
"""

import src.constants as _c
from src.entities.base import CollideActor


class Bolt(CollideActor):
    """A horizontal projectile fired by a Robot."""

    SPEED = 7

    def __init__(self, pos, dir_x: int):
        super().__init__(pos)
        self.direction_x = dir_x
        self.active = True

    def update(self) -> None:
        g = _c.current_game
        if self.move(self.direction_x, 0, Bolt.SPEED):
            # Hit a block or level edge
            self.active = False
        else:
            # Check collision with orbs and the player
            for obj in g.orbs + [g.player]:
                if obj and obj.hit_test(self):
                    self.active = False
                    break

        direction_idx = "1" if self.direction_x > 0 else "0"
        anim_frame = str((g.timer // 4) % 2)
        self.image = "bolt" + direction_idx + anim_frame