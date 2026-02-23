"""
game.py — The Game class.

Orchestrates a single play session: owns all entity lists, drives per-frame
updates, manages level transitions, renders the scene, and plays sounds.

All entity classes live in src/entities/.
All shared constants live in src/constants.py.
"""

from random import randint, shuffle

import src.constants as _c
from src.constants import (
    GRID_BLOCK_SIZE,
    LEVEL_X_OFFSET,
    LEVELS,
    NUM_COLUMNS,
    NUM_ROWS,
    WIDTH,
    set_current_game,
)
from src.entities.bolt import Bolt
from src.entities.fruit import Fruit
from src.entities.orb import Orb
from src.entities.pop import Pop
from src.entities.robot import Robot


class Game:
    """Manages a single play session (one player, N levels)."""

    def __init__(self, player=None):
        self.player = player
        self.level_colour = -1
        self.level = -1
        set_current_game(self)
        self.next_level()

    # ------------------------------------------------------------------
    # Difficulty scaling
    # ------------------------------------------------------------------

    def fire_probability(self) -> float:
        """Per-frame probability of a robot firing; increases with level."""
        return 0.001 + (0.0001 * min(100, self.level))

    def max_enemies(self) -> int:
        """Maximum simultaneous on-screen enemies; increases with level."""
        return min((self.level + 6) // 2, 8)

    # ------------------------------------------------------------------
    # Level lifecycle
    # ------------------------------------------------------------------

    def next_level(self) -> None:
        """Advance to the next level (or loop back after the last one)."""
        self.level_colour = (self.level_colour + 1) % 4
        self.level += 1

        self.grid = LEVELS[self.level % len(LEVELS)]
        # The last row mirrors the first row (used for wrap-around detection)
        self.grid = self.grid + [self.grid[0]]

        self.timer = -1

        if self.player:
            self.player.reset()

        self.fruits: list[Fruit] = []
        self.bolts: list[Bolt] = []
        self.enemies: list[Robot] = []
        self.pops: list[Pop] = []
        self.orbs: list[Orb] = []

        num_enemies = 10 + self.level
        num_strong = 1 + int(self.level / 1.5)
        num_weak = num_enemies - num_strong

        self.pending_enemies: list[int] = (
            num_strong * [Robot.TYPE_AGGRESSIVE] + num_weak * [Robot.TYPE_NORMAL]
        )
        shuffle(self.pending_enemies)

        self.play_sound("level", 1)

    def get_robot_spawn_x(self) -> float:
        """Find a free column at the top of the grid for a robot to spawn."""
        r = randint(0, NUM_COLUMNS - 1)
        for i in range(NUM_COLUMNS):
            grid_x = (r + i) % NUM_COLUMNS
            if self.grid[0][grid_x] == " ":
                return GRID_BLOCK_SIZE * grid_x + LEVEL_X_OFFSET + 12
        return WIDTH / 2

    # ------------------------------------------------------------------
    # Per-frame update
    # ------------------------------------------------------------------

    def update(self, input_state=None) -> None:
        """Advance the game by one frame.

        ``input_state`` is an InputState forwarded to the Player.  Pass
        None in menu / demo mode (player is not updated).
        """
        set_current_game(self)  # keep module-level reference current
        self.timer += 1

        # Update all entities
        for obj in self.fruits + self.bolts + self.enemies + self.pops + self.orbs:
            if obj:
                obj.update()

        if self.player and input_state is not None:
            self.player.update(input_state)

        # Prune expired / inactive entities
        self.fruits = [f for f in self.fruits if f.time_to_live > 0]
        self.bolts = [b for b in self.bolts if b.active]
        self.enemies = [e for e in self.enemies if e.alive]
        self.pops = [p for p in self.pops if p.timer < 12]
        self.orbs = [o for o in self.orbs if o.timer < 250 and o.y > -40]

        # Randomly spawn a fruit every 100 frames while enemies remain
        if self.timer % 100 == 0 and len(self.pending_enemies + self.enemies) > 0:
            self.fruits.append(Fruit((randint(70, 730), randint(75, 400))))

        # Spawn a queued robot every 81 frames if under the enemy cap
        if (
            self.timer % 81 == 0
            and len(self.pending_enemies) > 0
            and len(self.enemies) < self.max_enemies()
        ):
            robot_type = self.pending_enemies.pop()
            pos = (self.get_robot_spawn_x(), -30)
            self.enemies.append(Robot(pos, robot_type))

        # Advance to next level when all enemies and collectibles are gone
        if len(self.pending_enemies + self.fruits + self.enemies + self.pops) == 0:
            if not any(o.trapped_enemy_type is not None for o in self.orbs):
                self.next_level()

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def draw(self, screen) -> None:
        """Draw the background, level blocks, and all entities."""
        screen.blit("bg%d" % self.level_colour, (0, 0))

        block_sprite = "block" + str(self.level % 4)

        for row_y in range(NUM_ROWS):
            row = self.grid[row_y]
            if len(row) > 0:
                x = LEVEL_X_OFFSET
                for blk in row:
                    if blk != " ":
                        screen.blit(block_sprite, (x, row_y * GRID_BLOCK_SIZE))
                    x += GRID_BLOCK_SIZE

        all_objs = self.fruits + self.bolts + self.enemies + self.pops + self.orbs
        all_objs.append(self.player)
        for obj in all_objs:
            if obj:
                obj.draw()

    # ------------------------------------------------------------------
    # Audio
    # ------------------------------------------------------------------

    def play_sound(self, name: str, count: int = 1) -> None:
        """Play a named sound (with optional random variant) if audio is available."""
        if self.player and _c._sounds:
            try:
                sound = getattr(_c._sounds, name + str(randint(0, count - 1)))
                sound.play()
            except Exception as e:
                print(e)