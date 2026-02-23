"""
entities/base.py — Abstract base actor classes.

CollideActor  — Actor with block/wall collision.
GravityActor  — CollideActor that falls under gravity.
"""

from pgzero.actor import Actor

from src.constants import (
    ANCHOR_CENTRE,
    ANCHOR_CENTRE_BOTTOM,
    GRID_BLOCK_SIZE,
    HEIGHT,
    block,
    sign,
)


class CollideActor(Actor):
    """An Actor that can move with block and level-edge collision detection."""

    def __init__(self, pos, anchor=ANCHOR_CENTRE):
        super().__init__("blank", pos, anchor)

    def move(self, dx: int, dy: int, speed: int) -> bool:
        """Move the actor *speed* pixels in direction (dx, dy), one pixel at a
        time.  Returns True if movement was stopped by a block or level edge."""
        new_x, new_y = int(self.x), int(self.y)

        for _ in range(speed):
            new_x, new_y = new_x + dx, new_y + dy

            if new_x < 70 or new_x > 730:
                return True  # hit level edge

            if (
                (
                    dy > 0 and new_y % GRID_BLOCK_SIZE == 0
                    or dx > 0 and new_x % GRID_BLOCK_SIZE == 0
                    or dx < 0 and new_x % GRID_BLOCK_SIZE == GRID_BLOCK_SIZE - 1
                )
                and block(new_x, new_y)
            ):
                return True  # hit a block

            self.pos = new_x, new_y

        return False


class GravityActor(CollideActor):
    """A CollideActor that falls under gravity and can land on blocks."""

    MAX_FALL_SPEED = 10

    def __init__(self, pos):
        super().__init__(pos, ANCHOR_CENTRE_BOTTOM)
        self.vel_y = 0
        self.landed = False

    def update(self, detect: bool = True) -> None:
        """Apply gravity and optional collision detection.

        Pass ``detect=False`` when the actor should fall through the level
        (e.g. a dying player).
        """
        self.vel_y = min(self.vel_y + 1, GravityActor.MAX_FALL_SPEED)

        if detect:
            if self.move(0, sign(self.vel_y), abs(self.vel_y)):
                self.vel_y = 0
                self.landed = True

            if self.top >= HEIGHT:
                # Wrap around to the top of the screen
                self.y = 1
        else:
            self.y += self.vel_y