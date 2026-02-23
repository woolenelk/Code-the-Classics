"""
entities/pop.py — Pop (burst animation sprite).

Plays a short pop animation when an orb or fruit disappears.
"""

from pgzero.actor import Actor


class Pop(Actor):
    """A short animated sprite shown when an orb or fruit pops."""

    def __init__(self, pos, type_: int):
        super().__init__("blank", pos)
        self.type = type_
        self.timer = -1

    def update(self) -> None:
        self.timer += 1
        self.image = "pop" + str(self.type) + str(self.timer // 2)