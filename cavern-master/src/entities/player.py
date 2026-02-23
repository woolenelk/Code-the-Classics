"""
entities/player.py — Player character.

The Player is controlled via an InputState snapshot so it has no
direct dependency on the keyboard object.
"""

import src.constants as _c
from src.constants import HEIGHT, WIDTH
from src.entities.base import GravityActor
from src.entities.orb import Orb


class Player(GravityActor):
    """The player-controlled character."""

    def __init__(self):
        super().__init__((0, 0))
        self.lives = 2
        self.score = 0

    def reset(self) -> None:
        """Place the player at the starting position for a new life/level."""
        self.pos = (WIDTH / 2, 100)
        self.vel_y = 0
        self.direction_x = 1
        self.fire_timer = 0
        self.hurt_timer = 100  # brief invulnerability at the start
        self.health = 3
        self.blowing_orb = None

    def hit_test(self, other) -> bool:
        """Called by Bolt.update — returns True and applies damage if hit."""
        if self.collidepoint(other.pos) and self.hurt_timer < 0:
            self.hurt_timer = 200
            self.health -= 1
            self.vel_y = -12
            self.landed = False
            self.direction_x = other.direction_x
            if self.health > 0:
                _c.current_game.play_sound("ouch", 4)
            else:
                _c.current_game.play_sound("die")
            return True
        return False

    def update(self, input_state) -> None:
        """Update player state from a pre-built InputState snapshot.

        No keyboard access happens here — all edge/level detection is done
        centrally in InputHandler before this method is called.
        """
        g = _c.current_game
        # Collision detection is disabled when falling after death
        super().update(self.health > 0)

        self.fire_timer -= 1
        self.hurt_timer -= 1

        if self.landed:
            # After landing, reduce the post-hurt invulnerability window
            self.hurt_timer = min(self.hurt_timer, 100)

        dx = 0  # track horizontal direction for sprite selection below

        if self.hurt_timer > 100:
            # Recently hurt — recoil sideways or fall out of the level
            if self.health > 0:
                self.move(self.direction_x, 0, 4)
            else:
                if self.top >= HEIGHT * 1.5:
                    self.lives -= 1
                    self.reset()
        else:
            # --- Normal movement ---
            if input_state.left:
                dx = -1
            elif input_state.right:
                dx = 1

            if dx != 0:
                self.direction_x = dx
                if self.fire_timer < 10:
                    self.move(dx, 0, 4)

            # Fire orb on SPACE edge
            if input_state.fire_pressed and self.fire_timer <= 0 and len(g.orbs) < 5:
                x = min(730, max(70, self.x + self.direction_x * 38))
                y = self.y - 35
                self.blowing_orb = Orb((x, y), self.direction_x)
                g.orbs.append(self.blowing_orb)
                g.play_sound("blow", 4)
                self.fire_timer = 20

            # Jump on UP edge
            if input_state.jump_pressed and self.vel_y == 0 and self.landed:
                self.vel_y = -16
                self.landed = False
                g.play_sound("jump")

        # Blow current orb further while SPACE is held
        if input_state.fire_held:
            if self.blowing_orb:
                self.blowing_orb.blown_frames += 4
                if self.blowing_orb.blown_frames >= 120:
                    self.blowing_orb = None
        else:
            self.blowing_orb = None

        # --- Sprite selection ---
        self.image = "blank"
        if self.hurt_timer <= 0 or self.hurt_timer % 2 == 1:
            dir_index = "1" if self.direction_x > 0 else "0"
            if self.hurt_timer > 100:
                if self.health > 0:
                    self.image = "recoil" + dir_index
                else:
                    self.image = "fall" + str((g.timer // 4) % 2)
            elif self.fire_timer > 0:
                self.image = "blow" + dir_index
            elif dx == 0:
                self.image = "still"
            else:
                self.image = "run" + dir_index + str((g.timer // 8) % 4)