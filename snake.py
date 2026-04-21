#!/usr/bin/env python3
"""
Snake — a terminal Snake game built with Python curses.

Controls:
  Arrow keys or WASD  — move the snake
  P                   — pause / unpause
  Q                   — quit at any time
"""

import curses
import random
import time

# ── Layout ─────────────────────────────────────────────────────────────────────
BORDER_H = 1          # top/bottom border thickness in cells
BORDER_W = 2          # left/right border thickness in cells
MIN_ROWS  = 20
MIN_COLS  = 40

# ── Speed ──────────────────────────────────────────────────────────────────────
BASE_DELAY    = 0.15  # seconds between frames at level 1
SPEED_STEP    = 0.005 # reduce delay by this much per level gained
MIN_DELAY     = 0.04  # floor so the game stays playable

# ── Directions ─────────────────────────────────────────────────────────────────
UP    = (-1,  0)
DOWN  = ( 1,  0)
LEFT  = ( 0, -1)
RIGHT = ( 0,  1)

OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

KEY_MAP = {
    curses.KEY_UP:    UP,    ord('w'): UP,    ord('W'): UP,
    curses.KEY_DOWN:  DOWN,  ord('s'): DOWN,  ord('S'): DOWN,
    curses.KEY_LEFT:  LEFT,  ord('a'): LEFT,  ord('A'): LEFT,
    curses.KEY_RIGHT: RIGHT, ord('d'): RIGHT, ord('D'): RIGHT,
}

# ── Colors ─────────────────────────────────────────────────────────────────────
C_SNAKE_HEAD = 1
C_SNAKE_BODY = 2
C_FOOD       = 3
C_BORDER     = 4
C_STATUS     = 5
C_GAMEOVER   = 6


def init_colors() -> None:
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(C_SNAKE_HEAD, curses.COLOR_GREEN,   -1)
    curses.init_pair(C_SNAKE_BODY, curses.COLOR_CYAN,    -1)
    curses.init_pair(C_FOOD,       curses.COLOR_RED,     -1)
    curses.init_pair(C_BORDER,     curses.COLOR_YELLOW,  -1)
    curses.init_pair(C_STATUS,     curses.COLOR_WHITE,   -1)
    curses.init_pair(C_GAMEOVER,   curses.COLOR_MAGENTA, -1)


# ── Helpers ────────────────────────────────────────────────────────────────────

def draw_border(win: "curses.window", rows: int, cols: int) -> None:
    attr = curses.color_pair(C_BORDER) | curses.A_BOLD
    for r in range(rows):
        win.addch(r, 0,        '|', attr)
        win.addch(r, cols - 1, '|', attr)
    for c in range(cols):
        win.addch(0,        c, '-', attr)
        try:
            win.addch(rows - 1, c, '-', attr)
        except curses.error:
            pass


def place_food(snake: list, rows: int, cols: int) -> tuple:
    snake_set = set(snake)
    while True:
        r = random.randint(BORDER_H,     rows - BORDER_H - 1)
        c = random.randint(BORDER_W // 2, cols - BORDER_W // 2 - 1)
        pos = (r, c)
        if pos not in snake_set:
            return pos


def draw_status(win: "curses.window", cols: int, score: int, level: int,
                high: int, paused: bool) -> None:
    attr = curses.color_pair(C_STATUS)
    label = f" Score:{score:>5}  Level:{level:>2}  Best:{high:>5} "
    if paused:
        label += " [PAUSED] "
    try:
        win.addstr(0, max(0, (cols - len(label)) // 2), label, attr)
    except curses.error:
        pass


def show_splash(win: "curses.window", rows: int, cols: int) -> None:
    """Show start screen; wait for any key."""
    lines = [
        "╔══════════════════════╗",
        "║     S N A K E  🐍    ║",
        "╠══════════════════════╣",
        "║  Arrows / WASD: move ║",
        "║  P : pause           ║",
        "║  Q : quit            ║",
        "╠══════════════════════╣",
        "║   Press any key...   ║",
        "╚══════════════════════╝",
    ]
    start_r = (rows - len(lines)) // 2
    start_c = (cols - len(lines[0])) // 2
    attr = curses.color_pair(C_GAMEOVER) | curses.A_BOLD
    for i, line in enumerate(lines):
        try:
            win.addstr(start_r + i, max(0, start_c), line, attr)
        except curses.error:
            pass
    win.refresh()
    win.nodelay(False)
    win.getch()
    win.nodelay(True)


def show_game_over(win: "curses.window", rows: int, cols: int,
                   score: int, high: int) -> bool:
    """Return True if player wants to play again."""
    lines = [
        "╔══════════════════════╗",
        "║      GAME  OVER      ║",
        f"║   Your score: {score:>5}  ║",
        f"║   Best score: {high:>5}  ║",
        "╠══════════════════════╣",
        "║  R : play again      ║",
        "║  Q : quit            ║",
        "╚══════════════════════╝",
    ]
    start_r = (rows - len(lines)) // 2
    start_c = (cols - len(lines[0])) // 2
    attr = curses.color_pair(C_GAMEOVER) | curses.A_BOLD
    for i, line in enumerate(lines):
        try:
            win.addstr(start_r + i, max(0, start_c), line, attr)
        except curses.error:
            pass
    win.refresh()
    win.nodelay(False)
    while True:
        key = win.getch()
        if key in (ord('r'), ord('R')):
            return True
        if key in (ord('q'), ord('Q')):
            return False


# ── Core game loop ──────────────────────────────────────────────────────────────

def run_game(stdscr: "curses.window") -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    init_colors()

    rows, cols = stdscr.getmaxyx()
    if rows < MIN_ROWS or cols < MIN_COLS:
        stdscr.addstr(0, 0,
            f"Terminal too small. Need {MIN_COLS}x{MIN_ROWS}, "
            f"got {cols}x{rows}.")
        stdscr.refresh()
        time.sleep(3)
        return

    show_splash(stdscr, rows, cols)

    high_score = 0

    while True:   # outer: replay loop
        # ── Init state ──────────────────────────────────────────────────────
        mid_r, mid_c = rows // 2, cols // 2
        snake   = [(mid_r, mid_c + i) for i in range(3, -1, -1)]  # head first
        direction = RIGHT
        pending   = RIGHT
        food      = place_food(snake, rows, cols)
        score     = 0
        level     = 1
        paused    = False
        delay     = BASE_DELAY

        # ── Inner: one life ─────────────────────────────────────────────────
        while True:
            frame_start = time.monotonic()

            # --- input ---
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')):
                return
            if key in (ord('p'), ord('P')):
                paused = not paused
            if key in KEY_MAP:
                new_dir = KEY_MAP[key]
                if new_dir != OPPOSITES.get(direction):
                    pending = new_dir

            if paused:
                draw_border(stdscr, rows, cols)
                draw_status(stdscr, cols, score, level, high_score, paused)
                stdscr.refresh()
                time.sleep(0.05)
                continue

            direction = pending

            # --- move ---
            head_r, head_c = snake[0]
            dr, dc         = direction
            new_head       = (head_r + dr, head_c + dc)

            # wall collision
            if (new_head[0] <= 0 or new_head[0] >= rows - 1 or
                    new_head[1] <= 0 or new_head[1] >= cols - 1):
                break

            # self collision (skip tail tip because it moves away)
            if new_head in snake[:-1]:
                break

            snake.insert(0, new_head)

            # --- eat? ---
            if new_head == food:
                score += 10 * level
                high_score = max(high_score, score)
                food = place_food(snake, rows, cols)
                # level up every 5 foods eaten
                foods_eaten = score // (10 * level) if level == 1 else None
                new_level = 1 + score // 50
                if new_level != level:
                    level = new_level
                    delay = max(MIN_DELAY, BASE_DELAY - (level - 1) * SPEED_STEP)
            else:
                snake.pop()

            # --- draw ---
            stdscr.erase()
            draw_border(stdscr, rows, cols)
            draw_status(stdscr, cols, score, level, high_score, paused)

            # food
            try:
                stdscr.addch(food[0], food[1], '●',
                             curses.color_pair(C_FOOD) | curses.A_BOLD)
            except curses.error:
                pass

            # snake body
            for i, (r, c) in enumerate(snake):
                if i == 0:
                    ch   = '◉'
                    attr = curses.color_pair(C_SNAKE_HEAD) | curses.A_BOLD
                else:
                    ch   = '○'
                    attr = curses.color_pair(C_SNAKE_BODY)
                try:
                    stdscr.addch(r, c, ch, attr)
                except curses.error:
                    pass

            stdscr.refresh()

            # --- frame timing ---
            elapsed = time.monotonic() - frame_start
            sleep_t = delay - elapsed
            if sleep_t > 0:
                time.sleep(sleep_t)

        # ── Game over screen ─────────────────────────────────────────────────
        if not show_game_over(stdscr, rows, cols, score, high_score):
            break


def main() -> None:
    curses.wrapper(run_game)


if __name__ == "__main__":
    main()
