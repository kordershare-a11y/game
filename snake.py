#!/usr/bin/env python3
"""
Snake Game — a terminal-based snake game using the curses library.

Controls:
    Arrow keys or WASD to move
    P to pause/unpause
    Q to quit

Run:
    python3 snake.py
"""

import curses
import random
import time
from collections import deque
from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


OPPOSITE = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}

KEY_MAP = {
    curses.KEY_UP: Direction.UP,
    curses.KEY_DOWN: Direction.DOWN,
    curses.KEY_LEFT: Direction.LEFT,
    curses.KEY_RIGHT: Direction.RIGHT,
    ord("w"): Direction.UP,
    ord("W"): Direction.UP,
    ord("s"): Direction.DOWN,
    ord("S"): Direction.DOWN,
    ord("a"): Direction.LEFT,
    ord("A"): Direction.LEFT,
    ord("d"): Direction.RIGHT,
    ord("D"): Direction.RIGHT,
}

INITIAL_SPEED = 120  # ms per tick
MIN_SPEED = 60
SPEED_INCREMENT = 3  # ms faster per food eaten


class SnakeGame:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self._setup_curses()
        self.high_score = 0
        self._play_loop()

    def _setup_curses(self):
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)   # snake body
        curses.init_pair(2, curses.COLOR_RED, -1)      # food
        curses.init_pair(3, curses.COLOR_YELLOW, -1)   # border
        curses.init_pair(4, curses.COLOR_CYAN, -1)     # score / UI
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)  # snake head
        curses.init_pair(6, curses.COLOR_MAGENTA, -1)  # special food

    def _play_loop(self):
        while True:
            result = self._run_game()
            if result == "quit":
                return
            action = self._game_over_screen()
            if action == "quit":
                return

    def _init_game_state(self):
        max_y, max_x = self.stdscr.getmaxyx()
        self.board_h = max_y - 2  # leave room for score bar
        self.board_w = max_x
        if self.board_h < 10 or self.board_w < 20:
            raise RuntimeError("Terminal too small. Need at least 20x12.")

        mid_y = self.board_h // 2
        mid_x = self.board_w // 2
        self.snake = deque([(mid_y, mid_x - 2), (mid_y, mid_x - 1), (mid_y, mid_x)])
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.score = 0
        self.speed = INITIAL_SPEED
        self.food = None
        self.bonus_food = None
        self.bonus_timer = 0
        self._place_food()

    def _place_food(self):
        occupied = set(self.snake)
        if self.bonus_food:
            occupied.add(self.bonus_food)
        while True:
            pos = (random.randint(1, self.board_h - 2), random.randint(1, self.board_w - 2))
            if pos not in occupied:
                self.food = pos
                return

    def _place_bonus_food(self):
        occupied = set(self.snake)
        occupied.add(self.food)
        while True:
            pos = (random.randint(1, self.board_h - 2), random.randint(1, self.board_w - 2))
            if pos not in occupied:
                self.bonus_food = pos
                self.bonus_timer = 50  # ticks until it disappears
                return

    def _draw_border(self):
        attr = curses.color_pair(3)
        for x in range(self.board_w):
            self.stdscr.addch(0, x, "━", attr)
            try:
                self.stdscr.addch(self.board_h - 1, x, "━", attr)
            except curses.error:
                pass
        for y in range(self.board_h):
            self.stdscr.addch(y, 0, "┃", attr)
            try:
                self.stdscr.addch(y, self.board_w - 1, "┃", attr)
            except curses.error:
                pass
        self.stdscr.addch(0, 0, "┏", attr)
        try:
            self.stdscr.addch(0, self.board_w - 1, "┓", attr)
        except curses.error:
            pass
        self.stdscr.addch(self.board_h - 1, 0, "┗", attr)
        try:
            self.stdscr.addch(self.board_h - 1, self.board_w - 1, "┛", attr)
        except curses.error:
            pass

    def _draw_score_bar(self):
        bar_y = self.board_h
        attr = curses.color_pair(4) | curses.A_BOLD
        score_text = f" Score: {self.score}  |  High Score: {self.high_score}  |  Speed: {self.speed}ms "
        controls = " [Arrows/WASD] Move  [P] Pause  [Q] Quit "
        self.stdscr.addstr(bar_y, 0, " " * (self.board_w - 1), attr)
        self.stdscr.addstr(bar_y, 1, score_text, attr)
        right_start = self.board_w - len(controls) - 1
        if right_start > len(score_text) + 2:
            try:
                self.stdscr.addstr(bar_y, right_start, controls, attr)
            except curses.error:
                pass

    def _draw(self):
        self.stdscr.erase()
        self._draw_border()

        # Draw food
        fy, fx = self.food
        self.stdscr.addch(fy, fx, "●", curses.color_pair(2) | curses.A_BOLD)

        # Draw bonus food
        if self.bonus_food:
            by, bx = self.bonus_food
            self.stdscr.addch(by, bx, "★", curses.color_pair(6) | curses.A_BOLD)

        # Draw snake body
        body_chars = ["█", "▓", "▒"]
        for i, (sy, sx) in enumerate(self.snake):
            if i == len(self.snake) - 1:
                # Head
                self.stdscr.addch(sy, sx, "◆", curses.color_pair(5) | curses.A_BOLD)
            else:
                dist_from_head = len(self.snake) - 1 - i
                char_idx = min(dist_from_head // 4, len(body_chars) - 1)
                self.stdscr.addch(sy, sx, body_chars[char_idx], curses.color_pair(1))

        self._draw_score_bar()
        self.stdscr.refresh()

    def _run_game(self) -> str:
        self._init_game_state()
        self.stdscr.timeout(self.speed)
        foods_eaten = 0

        while True:
            self._draw()

            key = self.stdscr.getch()

            if key == ord("q") or key == ord("Q"):
                return "quit"
            if key == ord("p") or key == ord("P"):
                self._pause()
                continue

            if key in KEY_MAP:
                new_dir = KEY_MAP[key]
                if new_dir != OPPOSITE.get(self.direction):
                    self.next_direction = new_dir

            self.direction = self.next_direction
            dy, dx = self.direction.value
            head_y, head_x = self.snake[-1]
            new_head = (head_y + dy, head_x + dx)

            # Collision with walls
            if (new_head[0] <= 0 or new_head[0] >= self.board_h - 1 or
                    new_head[1] <= 0 or new_head[1] >= self.board_w - 1):
                return "dead"

            # Collision with self
            if new_head in set(self.snake):
                return "dead"

            self.snake.append(new_head)

            ate = False
            if new_head == self.food:
                self.score += 10
                foods_eaten += 1
                self.speed = max(MIN_SPEED, INITIAL_SPEED - foods_eaten * SPEED_INCREMENT)
                self.stdscr.timeout(self.speed)
                self._place_food()
                ate = True
                if foods_eaten % 5 == 0 and not self.bonus_food:
                    self._place_bonus_food()

            if self.bonus_food and new_head == self.bonus_food:
                self.score += 50
                self.bonus_food = None
                self.bonus_timer = 0
                ate = True

            if not ate:
                self.snake.popleft()

            # Tick down bonus food
            if self.bonus_food:
                self.bonus_timer -= 1
                if self.bonus_timer <= 0:
                    self.bonus_food = None

            if self.score > self.high_score:
                self.high_score = self.score

    def _pause(self):
        attr = curses.color_pair(4) | curses.A_BOLD
        msg = "  PAUSED — Press P to resume  "
        y = self.board_h // 2
        x = max(0, (self.board_w - len(msg)) // 2)
        self.stdscr.addstr(y, x, msg, attr | curses.A_REVERSE)
        self.stdscr.refresh()
        self.stdscr.timeout(-1)
        while True:
            key = self.stdscr.getch()
            if key == ord("p") or key == ord("P"):
                self.stdscr.timeout(self.speed)
                return
            if key == ord("q") or key == ord("Q"):
                raise SystemExit

    def _game_over_screen(self) -> str:
        self.stdscr.erase()
        max_y, max_x = self.stdscr.getmaxyx()
        cx = max_x // 2
        cy = max_y // 2

        title_attr = curses.color_pair(2) | curses.A_BOLD
        info_attr = curses.color_pair(4)
        prompt_attr = curses.color_pair(3) | curses.A_BOLD

        lines = [
            ("╔══════════════════════════╗", title_attr),
            ("║       GAME  OVER         ║", title_attr),
            ("╚══════════════════════════╝", title_attr),
            ("", 0),
            (f"Score: {self.score}", info_attr | curses.A_BOLD),
            (f"High Score: {self.high_score}", info_attr),
            ("", 0),
            ("[R] Play Again   [Q] Quit", prompt_attr),
        ]

        for i, (text, attr) in enumerate(lines):
            y = cy - len(lines) // 2 + i
            x = cx - len(text) // 2
            if 0 <= y < max_y and 0 <= x < max_x:
                try:
                    self.stdscr.addstr(y, x, text, attr)
                except curses.error:
                    pass

        self.stdscr.refresh()
        self.stdscr.timeout(-1)
        while True:
            key = self.stdscr.getch()
            if key == ord("r") or key == ord("R"):
                return "restart"
            if key == ord("q") or key == ord("Q"):
                return "quit"


def main(stdscr):
    SnakeGame(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
