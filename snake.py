#!/usr/bin/env python3
"""
Terminal Snake — arrow keys to move, q to quit, r to restart after game over.
Requires a terminal with curses (Linux / macOS).
"""

from __future__ import annotations

import curses
import random
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    y: int
    x: int


def main() -> None:
    curses.wrapper(run)


def run(stdscr: curses.window) -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    h, w = stdscr.getmaxyx()
    if h < 12 or w < 24:
        stdscr.addstr(0, 0, "Terminal too small (need at least 24x12).")
        stdscr.nodelay(False)
        stdscr.getch()
        return

    play(stdscr)


def play(stdscr: curses.window) -> None:
    h, w = stdscr.getmaxyx()
    # Inner field (leave border)
    top, left = 1, 1
    bottom, right = h - 2, w - 2
    field_h = bottom - top + 1
    field_w = right - left + 1

    snake = [
        Point(top + field_h // 2, left + field_w // 2),
        Point(top + field_h // 2, left + field_w // 2 - 1),
        Point(top + field_h // 2, left + field_w // 2 - 2),
    ]
    direction = (0, 1)  # dy, dx
    pending_dir: tuple[int, int] | None = None
    score = 0
    tick = 0.12

    def random_food() -> Point:
        while True:
            fy = random.randint(top, bottom)
            fx = random.randint(left, right)
            p = Point(fy, fx)
            if p not in snake:
                return p

    food = random_food()
    game_over = False

    def draw_border() -> None:
        stdscr.erase()
        title = " Snake — arrows move | q quit | r restart "
        try:
            stdscr.addnstr(0, max(0, (w - len(title)) // 2), title, w - 1)
        except curses.error:
            pass

    def draw() -> None:
        draw_border()
        status = f" Score: {score} "
        try:
            stdscr.addnstr(h - 1, max(0, w - len(status) - 1), status, w - 1)
        except curses.error:
            pass
        for i, seg in enumerate(snake):
            ch = "@" if i == 0 else "o"
            try:
                stdscr.addch(seg.y, seg.x, ord(ch))
            except curses.error:
                pass
        try:
            stdscr.addch(food.y, food.x, ord("*"))
        except curses.error:
            pass
        if game_over:
            msg = " GAME OVER — r restart | q quit "
            try:
                stdscr.addnstr(h // 2, max(0, (w - len(msg)) // 2), msg, w - 1)
            except curses.error:
                pass
        stdscr.refresh()

    last = time.monotonic()
    while True:
        now = time.monotonic()
        if now - last < tick:
            ch = stdscr.getch()
            if ch == ord("q"):
                return
            if game_over and ch == ord("r"):
                play(stdscr)
                return
            if ch in (curses.KEY_UP, ord("k")):
                pending_dir = (-1, 0)
            elif ch in (curses.KEY_DOWN, ord("j")):
                pending_dir = (1, 0)
            elif ch in (curses.KEY_LEFT, ord("h")):
                pending_dir = (0, -1)
            elif ch in (curses.KEY_RIGHT, ord("l")):
                pending_dir = (0, 1)
            time.sleep(0.01)
            continue
        last = now

        ch = stdscr.getch()
        if ch == ord("q"):
            return
        if game_over:
            if ch == ord("r"):
                play(stdscr)
                return
            draw()
            continue

        if ch in (curses.KEY_UP, ord("k")):
            pending_dir = (-1, 0)
        elif ch in (curses.KEY_DOWN, ord("j")):
            pending_dir = (1, 0)
        elif ch in (curses.KEY_LEFT, ord("h")):
            pending_dir = (0, -1)
        elif ch in (curses.KEY_RIGHT, ord("l")):
            pending_dir = (0, 1)

        if pending_dir is not None:
            dy, dx = pending_dir
            if (dy + direction[0], dx + direction[1]) != (0, 0):
                direction = pending_dir
            pending_dir = None

        dy, dx = direction
        head = snake[0]
        new_head = Point(head.y + dy, head.x + dx)

        if not (top <= new_head.y <= bottom and left <= new_head.x <= right):
            game_over = True
            draw()
            continue
        if new_head in snake:
            game_over = True
            draw()
            continue

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = random_food()
            tick = max(0.05, tick - 0.004)
        else:
            snake.pop()

        draw()


if __name__ == "__main__":
    main()
