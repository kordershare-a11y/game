# Neon Snake

A polished, modern take on the classic Snake game. Built as a single HTML file —
no build step, no dependencies. Just open and play.

## Play

Open `index.html` in any modern browser. That's it.

On macOS/Linux you can run:

```bash
xdg-open index.html   # Linux
open index.html       # macOS
```

Or serve the folder locally if you prefer:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Features

- Smooth, frame-rate independent game loop (fixed-timestep ticks)
- Arrow keys or **WASD** to move; **Space** to pause/resume; **R** to reset
- Swipe gestures on touch devices
- Gradual speed-up as you score
- Glow, pulse, and eat-flash effects on an HTML canvas
- Subtle WebAudio sound effects (toggle with the Sound button)
- Persistent best-score saved to `localStorage`
- Auto-pause when the tab loses focus
- Fully responsive, works on phones and desktops

## Controls

| Action         | Keyboard                | Touch               |
| -------------- | ----------------------- | ------------------- |
| Move           | Arrow keys / WASD       | Swipe in direction  |
| Pause / resume | Space                   | Tap the board       |
| Reset          | R, or the Reset button  | Reset button        |
| Mute / unmute  | Sound button            | Sound button        |

Enjoy!
