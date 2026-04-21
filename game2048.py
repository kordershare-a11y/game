from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, List, Sequence


Direction = str


def merge_line(line: Sequence[int]) -> tuple[list[int], int, bool]:
    """Slide non-zero values left and merge equal neighbors once."""
    values = [value for value in line if value]
    merged: list[int] = []
    score_gain = 0
    index = 0

    while index < len(values):
        current = values[index]
        if index + 1 < len(values) and values[index + 1] == current:
            current *= 2
            score_gain += current
            index += 2
        else:
            index += 1
        merged.append(current)

    merged.extend([0] * (len(line) - len(merged)))
    return merged, score_gain, merged != list(line)


def transpose(board: Sequence[Sequence[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*board)]


def reverse_rows(board: Sequence[Sequence[int]]) -> list[list[int]]:
    return [list(reversed(row)) for row in board]


@dataclass
class MoveResult:
    changed: bool
    score_gain: int


class Game2048:
    def __init__(self, size: int = 4, seed: int | None = None) -> None:
        self.size = size
        self.random = random.Random(seed)
        self.score = 0
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.add_random_tile()
        self.add_random_tile()

    def reset(self) -> None:
        self.score = 0
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self) -> bool:
        empty_cells = [
            (row_index, column_index)
            for row_index, row in enumerate(self.board)
            for column_index, value in enumerate(row)
            if value == 0
        ]

        if not empty_cells:
            return False

        row_index, column_index = self.random.choice(empty_cells)
        self.board[row_index][column_index] = 4 if self.random.random() < 0.1 else 2
        return True

    def has_won(self) -> bool:
        return any(value >= 2048 for row in self.board for value in row)

    def can_move(self) -> bool:
        for row in self.board:
            if 0 in row:
                return True

        for row_index in range(self.size):
            for column_index in range(self.size):
                value = self.board[row_index][column_index]
                if row_index + 1 < self.size and self.board[row_index + 1][column_index] == value:
                    return True
                if column_index + 1 < self.size and self.board[row_index][column_index + 1] == value:
                    return True

        return False

    def move(self, direction: Direction, *, spawn: bool = True) -> MoveResult:
        if direction not in {"left", "right", "up", "down"}:
            raise ValueError(f"Unsupported direction: {direction}")

        working_board = [row[:] for row in self.board]

        if direction == "up":
            working_board = transpose(working_board)
        elif direction == "down":
            working_board = reverse_rows(transpose(working_board))
        elif direction == "right":
            working_board = reverse_rows(working_board)

        updated_board: list[list[int]] = []
        total_score_gain = 0
        any_changed = False

        for row in working_board:
            merged_row, score_gain, changed = merge_line(row)
            updated_board.append(merged_row)
            total_score_gain += score_gain
            any_changed = any_changed or changed

        if direction == "up":
            updated_board = transpose(updated_board)
        elif direction == "down":
            updated_board = transpose(reverse_rows(updated_board))
        elif direction == "right":
            updated_board = reverse_rows(updated_board)

        if any_changed:
            self.board = updated_board
            self.score += total_score_gain
            if spawn:
                self.add_random_tile()

        return MoveResult(changed=any_changed, score_gain=total_score_gain)

    def render(self) -> str:
        largest_value = max(max(row) for row in self.board)
        cell_width = max(5, len(str(largest_value)) + 2)
        horizontal = "+" + "+".join("-" * cell_width for _ in range(self.size)) + "+"
        lines = [f"Score: {self.score}", horizontal]

        for row in self.board:
            rendered_cells = [f"{value or '.':^{cell_width}}" for value in row]
            lines.append("|" + "|".join(rendered_cells) + "|")
            lines.append(horizontal)

        return "\n".join(lines)


def parse_direction(command: str) -> Direction | None:
    lookup = {
        "w": "up",
        "up": "up",
        "a": "left",
        "left": "left",
        "s": "down",
        "down": "down",
        "d": "right",
        "right": "right",
    }
    return lookup.get(command.strip().lower())


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def play() -> None:
    game = Game2048()
    message = "Combine tiles with W/A/S/D. Reach 2048 to win."
    celebrated_win = False

    while True:
        clear_screen()
        print("2048\n")
        print(game.render())
        print("\nControls: W/A/S/D to move, N for a new game, Q to quit.")
        print(message)

        if game.has_won() and not celebrated_win:
            print("You made 2048! You can keep playing for a higher score.")
            celebrated_win = True

        if not game.can_move():
            print("No more legal moves. Press N to restart or Q to quit.")

        command = input("> ").strip().lower()

        if command == "q":
            print("Thanks for playing!")
            return

        if command == "n":
            game.reset()
            celebrated_win = False
            message = "Started a new game."
            continue

        direction = parse_direction(command)
        if direction is None:
            message = "Unknown command. Use W/A/S/D, N, or Q."
            continue

        if not game.can_move():
            message = "The board is locked. Start a new game with N or quit with Q."
            continue

        result = game.move(direction)
        if result.changed:
            message = f"Moved {direction}. Score +{result.score_gain}."
        else:
            message = "That move does not change the board. Try another direction."


if __name__ == "__main__":
    play()
