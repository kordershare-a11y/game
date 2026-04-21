# game

Meteor Sprint is a small browser arcade game you can run locally with no build step.

## How to play

1. Open `index.html` in a browser.
2. Click **Start game** or press **Space**.
3. Move with **Arrow keys** or **WASD**.
4. Dodge meteors, collect stars, and survive as long as possible.

## Rules

- You start with 3 shields.
- Hitting a meteor costs 1 shield.
- Collecting a star increases your score and star count.
- Every 5 stars repairs 1 shield, up to the maximum.
- Your best score is saved in the browser.

## Optional local server

If you prefer serving the files instead of opening them directly:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.
