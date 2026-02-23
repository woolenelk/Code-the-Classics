# Cavern — Refactored

A refactored version of the Pygame Zero Bubble Bobble clone from
[Wireframe Magazine / Code the Classics](https://github.com/Wireframe-Magazine/Code-the-Classics/tree/master/cavern-master).

Gameplay is **identical** to the original.  The refactoring improves structure
without changing controls, scoring, enemy behaviour, or level progression.

---

## How to Run

### Prerequisites

```bash
pip install pgzero          # installs pygame as a dependency too
```

Python ≥ 3.5 and Pygame Zero ≥ 1.2 are required.

### Assets

Copy the original `images/` and `sounds/` folders from the upstream repo into
the project root (next to `main.py`).  The game will not start without them.

### Start the game

```bash
cd cavern            # project root — the directory containing main.py
python main.py
```

Controls:

| Key | Action |
|-----|--------|
| ← / → | Move |
| ↑ | Jump |
| SPACE (press) | Fire orb |
| SPACE (hold) | Blow orb further |
| P | Pause / Resume |
| SPACE (menu / game over) | Confirm / continue |

---

## How to Run Tests

```bash
pip install pytest
pytest tests/
```

The test suite exercises the InputHandler edge-detection logic and the
App screen-transition API without requiring a display or Pygame Zero runtime.

---

## Architectural Changes

The original single-file `cavern.py` (~784 lines) has been split into a small
module tree:

```
main.py              ← Pygame Zero entry point (thin delegate)
src/
  app.py             ← App: owns the current screen, handles transitions
  input.py           ← InputHandler + InputState dataclass
  game.py            ← Game class + all entity classes (Game logic unchanged)
  screens/
    menu.py          ← MenuScreen
    play.py          ← PlayScreen (includes pause overlay)
    game_over.py     ← GameOverScreen
```

### Task A — State pattern
`App` owns the active screen object and exposes `change_screen(name)`.  The
global `update()` and `draw()` are one-liners that call `app.update()` /
`app.draw()`.  Each screen implements `update(input_state, app)` and
`draw(screen)`.  No `if state == ...` branching remains in the global
functions.

### Task B — Input snapshot
`InputHandler.snapshot(keyboard)` is called once per frame and returns a
frozen `InputState` dataclass.  No other module reads `keyboard.*` directly.
Edge detection (fire_pressed, jump_pressed, pause_pressed) is centralised here.
The global `space_down` variable and `space_pressed()` function are gone.
`Player.update(input_state)` consumes the snapshot.

### Task C — Pause
`PlayScreen` tracks a `_paused` boolean toggled by `input_state.pause_pressed`
(P key edge).  While paused the game simulation is frozen; `draw()` still
renders the play scene plus a semi-transparent "PAUSED" overlay.  Pause is
only available in `PlayScreen` — it cannot be triggered on the menu or game-over
screen.