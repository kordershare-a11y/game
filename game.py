#!/usr/bin/env python3
"""Terminal Tic-Tac-Toe game: player vs computer."""

import random


WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def render_cell(board, index):
    return board[index] if board[index] != " " else str(index + 1)


def print_board(board):
    print()
    print(f" {render_cell(board, 0)} | {render_cell(board, 1)} | {render_cell(board, 2)} ")
    print("---+---+---")
    print(f" {render_cell(board, 3)} | {render_cell(board, 4)} | {render_cell(board, 5)} ")
    print("---+---+---")
    print(f" {render_cell(board, 6)} | {render_cell(board, 7)} | {render_cell(board, 8)} ")
    print()


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    if " " not in board:
        return "draw"
    return None


def player_move(board):
    while True:
        try:
            raw = input("Choose a square (1-9): ").strip()
        except EOFError:
            print("\nInput ended. Exiting game.")
            raise SystemExit(0)
        if raw not in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}:
            print("Please enter a number from 1 to 9.")
            continue
        idx = int(raw) - 1
        if board[idx] != " ":
            print("That square is already taken.")
            continue
        board[idx] = "X"
        return


def available_moves(board):
    return [i for i, mark in enumerate(board) if mark == " "]


def computer_move(board):
    # Priority: win now, block player, center, corner, side.
    for move in available_moves(board):
        trial = board[:]
        trial[move] = "O"
        if winner(trial) == "O":
            board[move] = "O"
            return

    for move in available_moves(board):
        trial = board[:]
        trial[move] = "X"
        if winner(trial) == "X":
            board[move] = "O"
            return

    if board[4] == " ":
        board[4] = "O"
        return

    corners = [i for i in (0, 2, 6, 8) if board[i] == " "]
    if corners:
        board[random.choice(corners)] = "O"
        return

    sides = [i for i in (1, 3, 5, 7) if board[i] == " "]
    board[random.choice(sides)] = "O"


def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print("You are X. The computer is O.")
    board = [" "] * 9
    current = "X"

    while True:
        print_board(board)
        if current == "X":
            player_move(board)
        else:
            print("Computer is thinking...")
            computer_move(board)

        result = winner(board)
        if result:
            print_board(board)
            if result == "draw":
                print("It's a draw.")
            elif result == "X":
                print("You win!")
            else:
                print("Computer wins.")
            return

        current = "O" if current == "X" else "X"


def main():
    while True:
        play_game()
        try:
            again = input("Play again? (y/n): ").strip().lower()
        except EOFError:
            print("\nInput ended. Exiting game.")
            break
        if again != "y":
            print("Thanks for playing.")
            break


if __name__ == "__main__":
    main()
