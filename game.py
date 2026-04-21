#!/usr/bin/env python3
"""Terminal Tic-Tac-Toe with configurable AI difficulty."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def display_board(board: list[str]) -> None:
    """Render the board, showing move numbers on empty squares."""

    def cell(index: int) -> str:
        value = board[index]
        return value if value != " " else str(index + 1)

    print()
    print(f" {cell(0)} | {cell(1)} | {cell(2)} ")
    print("---+---+---")
    print(f" {cell(3)} | {cell(4)} | {cell(5)} ")
    print("---+---+---")
    print(f" {cell(6)} | {cell(7)} | {cell(8)} ")
    print()


def available_moves(board: list[str]) -> list[int]:
    return [index + 1 for index, value in enumerate(board) if value == " "]


def check_winner(board: list[str]) -> Optional[str]:
    for i, j, k in WINNING_LINES:
        if board[i] == board[j] == board[k] != " ":
            return board[i]
    if all(value != " " for value in board):
        return "Draw"
    return None


def minimax(
    board: list[str], ai_symbol: str, player_symbol: str, maximizing: bool
) -> int:
    result = check_winner(board)
    if result == ai_symbol:
        return 1
    if result == player_symbol:
        return -1
    if result == "Draw":
        return 0

    if maximizing:
        best_score = -999
        for move in available_moves(board):
            board[move - 1] = ai_symbol
            score = minimax(board, ai_symbol, player_symbol, maximizing=False)
            board[move - 1] = " "
            best_score = max(best_score, score)
        return best_score

    best_score = 999
    for move in available_moves(board):
        board[move - 1] = player_symbol
        score = minimax(board, ai_symbol, player_symbol, maximizing=True)
        board[move - 1] = " "
        best_score = min(best_score, score)
    return best_score


def best_move(board: list[str], ai_symbol: str, player_symbol: str) -> int:
    top_score = -999
    top_move = available_moves(board)[0]
    for move in available_moves(board):
        board[move - 1] = ai_symbol
        score = minimax(board, ai_symbol, player_symbol, maximizing=False)
        board[move - 1] = " "
        if score > top_score:
            top_score = score
            top_move = move
    return top_move


def prompt_choice(prompt: str, valid_choices: set[str]) -> str:
    while True:
        choice = input(prompt).strip().upper()
        if choice in valid_choices:
            return choice
        valid_options = ", ".join(sorted(valid_choices))
        print(f"Invalid input. Choose one of: {valid_options}")


@dataclass
class Scoreboard:
    player: int = 0
    computer: int = 0
    draws: int = 0


class TicTacToeGame:
    def __init__(self) -> None:
        self.player_symbol = "X"
        self.computer_symbol = "O"
        self.difficulty = "MEDIUM"
        self.scoreboard = Scoreboard()

    def setup(self) -> None:
        print("=== Tic-Tac-Toe ===")
        self.player_symbol = prompt_choice("Choose your symbol (X/O): ", {"X", "O"})
        self.computer_symbol = "O" if self.player_symbol == "X" else "X"
        self.difficulty = prompt_choice(
            "Difficulty (easy/medium/hard): ", {"EASY", "MEDIUM", "HARD"}
        )
        print(
            f"You are {self.player_symbol}. Computer is {self.computer_symbol}. "
            f"Difficulty: {self.difficulty.title()}."
        )

    def get_player_move(self, board: list[str]) -> int:
        valid_moves = set(available_moves(board))
        while True:
            raw = input(f"Your move ({'/'.join(map(str, sorted(valid_moves)))}): ").strip()
            if raw.isdigit():
                move = int(raw)
                if move in valid_moves:
                    return move
            print("That move is not available.")

    def get_computer_move(self, board: list[str]) -> int:
        moves = available_moves(board)
        if self.difficulty == "EASY":
            return random.choice(moves)
        if self.difficulty == "MEDIUM":
            if random.random() < 0.7:
                return best_move(board, self.computer_symbol, self.player_symbol)
            return random.choice(moves)
        return best_move(board, self.computer_symbol, self.player_symbol)

    def play_round(self) -> str:
        board = [" "] * 9
        turn = "X"

        while True:
            display_board(board)
            if turn == self.player_symbol:
                move = self.get_player_move(board)
            else:
                move = self.get_computer_move(board)
                print(f"Computer chooses: {move}")

            board[move - 1] = turn
            result = check_winner(board)
            if result:
                display_board(board)
                if result == "Draw":
                    print("It's a draw.")
                elif result == self.player_symbol:
                    print("You win this round!")
                else:
                    print("Computer wins this round.")
                return result

            turn = "O" if turn == "X" else "X"

    def update_score(self, result: str) -> None:
        if result == self.player_symbol:
            self.scoreboard.player += 1
        elif result == self.computer_symbol:
            self.scoreboard.computer += 1
        else:
            self.scoreboard.draws += 1

    def show_score(self) -> None:
        print(
            "Score -> "
            f"You: {self.scoreboard.player} | "
            f"Computer: {self.scoreboard.computer} | "
            f"Draws: {self.scoreboard.draws}"
        )


def main() -> None:
    game = TicTacToeGame()
    game.setup()

    while True:
        result = game.play_round()
        game.update_score(result)
        game.show_score()
        play_again = prompt_choice("Play again? (y/n): ", {"Y", "N"})
        if play_again == "N":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
