# Snake Game

A classic Snake game that runs in your terminal, built with Python and the `curses` library.

![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue)

## How to Play

```bash
python3 snake.py
```

### Controls

| Key              | Action       |
|------------------|--------------|
| Arrow keys / WASD | Move         |
| P                | Pause        |
| Q                | Quit         |
| R                | Restart (on game over) |

### Gameplay

- Guide the snake to eat food (`●`) to grow and earn **10 points**.
- Every 5 foods eaten, a bonus star (`★`) appears for a limited time — worth **50 points**.
- The game speeds up as you eat more food.
- Don't crash into the walls or yourself!
- Your high score is tracked across rounds within the same session.

## Requirements

- Python 3.6+
- A terminal that supports curses (Linux, macOS, or WSL on Windows)
- No external dependencies — uses only the Python standard library.
