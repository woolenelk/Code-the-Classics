"""
entities/fruit.py — Fruit (pickup spawned when a trapped orb pops).

Fruits fall under gravity, can be collected by the Player for points
or power-ups, and disappear after a fixed lifetime.
"""

from random import choice

import src.constants as _c
from src.constants import ROBOT_TYPE_NORMAL
from src.entities.base import GravityActor
from src.entities.pop import Pop


class Fruit(GravityActor):
    """A collectible pickup that falls from a burst orb or spawns randomly."""

    APPLE = 0
    RASPBERRY = 1
    LEMON = 2
    EXTRA_HEALTH = 3
    EXTRA_LIFE = 4

    def __init__(self, pos, trapped_enemy_type: int = 0):
        super().__init__(pos)

        # Fruit type depends on what kind of Robot was trapped
        if trapped_enemy_type == ROBOT_TYPE_NORMAL:
            self.type = choice([Fruit.APPLE, Fruit.RASPBERRY, Fruit.LEMON])
        else:
            # More dangerous robot type → chance of power-up
            types = 10 * [Fruit.APPLE, Fruit.RASPBERRY, Fruit.LEMON]
            types += 9 * [Fruit.EXTRA_HEALTH]
            types += [Fruit.EXTRA_LIFE]
            self.type = choice(types)

        self.time_to_live = 500

    def update(self) -> None:
        g = _c.current_game
        super().update()

        if g.player and g.player.collidepoint(self.center):
            # Player collected this fruit
            if self.type == Fruit.EXTRA_HEALTH:
                g.player.health = min(3, g.player.health + 1)
                g.play_sound("bonus")
            elif self.type == Fruit.EXTRA_LIFE:
                g.player.lives += 1
                g.play_sound("bonus")
            else:
                g.player.score += (self.type + 1) * 100
                g.play_sound("score")
            self.time_to_live = 0
        else:
            self.time_to_live -= 1

        if self.time_to_live <= 0:
            g.pops.append(Pop((self.x, self.y - 27), 0))

        anim_frame = str([0, 1, 2, 1][(g.timer // 6) % 4])
        self.image = "fruit" + str(self.type) + anim_frame