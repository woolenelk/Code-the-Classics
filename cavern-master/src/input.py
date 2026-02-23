"""
input.py — Centralised input snapshot with edge detection.

InputHandler.snapshot() is called once per frame and returns an
InputState dataclass.  No other module reads keyboard.* directly.
"""

from dataclasses import dataclass, field


@dataclass
class InputState:
    # Held directions
    left: bool = False
    right: bool = False
    up: bool = False

    # Edge-detected (True only on the frame the key was first pressed)
    jump_pressed: bool = False   # UP key edge
    fire_pressed: bool = False   # SPACE key edge  – fires an orb / starts game
    pause_pressed: bool = False  # P key edge      – toggles pause

    # Level (held)
    fire_held: bool = False      # SPACE held      – blows the current orb further


class InputHandler:
    """Converts raw Pygame Zero keyboard state into an InputState snapshot."""

    def __init__(self):
        self._prev_space = False
        self._prev_p = False
        self._prev_up = False

    def snapshot(self, keyboard) -> InputState:
        space_now = bool(keyboard.space)
        p_now = bool(keyboard.p)
        up_now = bool(keyboard.up)

        state = InputState(
            left=bool(keyboard.left),
            right=bool(keyboard.right),
            up=up_now,
            jump_pressed=up_now and not self._prev_up,
            fire_pressed=space_now and not self._prev_space,
            fire_held=space_now,
            pause_pressed=p_now and not self._prev_p,
        )

        self._prev_space = space_now
        self._prev_p = p_now
        self._prev_up = up_now

        return state