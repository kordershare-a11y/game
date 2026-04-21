# Snake Game 🐍

A classic Snake game that runs in your terminal, written in Python using the built-in `curses` library — no extra dependencies required.

## Requirements

- Python 3.6+
- A terminal that supports `curses` (any Linux/macOS terminal; on Windows use WSL or Git Bash)

## How to run

```bash
python3 snake.py
```

## Controls

| Key               | Action          |
|-------------------|-----------------|
| Arrow keys / WASD | Move the snake  |
| P                 | Pause / unpause |
| Q                 | Quit            |
| R (game-over)     | Play again      |

## Gameplay

- Eat the red **●** food to grow and score points.
- Avoid hitting the walls or the snake's own body.
- The snake speeds up as your level increases (every 50 points = +1 level).
- Your best score is tracked for the session.

## Tips

- Make sure your terminal window is at least **40 columns × 20 rows** before launching.
- Resize the window before starting a new game if needed.
