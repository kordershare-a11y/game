"""Terminal number guessing game.

Run with: python3 game.py
"""

from __future__ import annotations

import random


DIFFICULTIES = {
    "1": ("Easy", 20, 6),
    "2": ("Medium", 50, 8),
    "3": ("Hard", 100, 10),
}


def choose_difficulty() -> tuple[str, int, int]:
    """Prompt for a difficulty and return its settings."""
    print("\nChoose a difficulty:")
    for key, (name, upper_bound, attempts) in DIFFICULTIES.items():
        print(f"  {key}) {name} (1-{upper_bound}, {attempts} attempts)")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("Please choose 1, 2, or 3.")


def read_guess(upper_bound: int) -> int:
    """Read and validate one guess."""
    while True:
        raw_guess = input(f"Enter your guess (1-{upper_bound}): ").strip()
        if not raw_guess.isdigit():
            print("Use digits only.")
            continue

        guess = int(raw_guess)
        if 1 <= guess <= upper_bound:
            return guess

        print(f"Your guess must be between 1 and {upper_bound}.")


def play_round() -> int:
    """Play one round and return earned points."""
    name, upper_bound, max_attempts = choose_difficulty()
    target = random.randint(1, upper_bound)

    print(f"\n--- {name} Round ---")
    print(f"I picked a number between 1 and {upper_bound}.")
    print(f"You have {max_attempts} attempts.\n")

    for attempt in range(1, max_attempts + 1):
        guess = read_guess(upper_bound)

        if guess == target:
            points = (max_attempts - attempt + 1) * 10
            print(f"Correct! You guessed it in {attempt} attempts.")
            print(f"You earned {points} points this round.\n")
            return points

        direction = "higher" if guess < target else "lower"
        remaining = max_attempts - attempt
        print(f"Nope. Try {direction}. Remaining attempts: {remaining}")

    print(f"\nOut of attempts! The number was {target}.\n")
    return 0


def ask_play_again() -> bool:
    """Return True when user wants another round."""
    while True:
        answer = input("Play another round? (y/n): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter y or n.")


def main() -> None:
    print("=== Number Quest ===")
    print("Guess the hidden number before you run out of attempts.")

    total_score = 0
    rounds_played = 0
    rounds_won = 0

    while True:
        points = play_round()
        rounds_played += 1
        total_score += points
        if points > 0:
            rounds_won += 1

        print("=== Session Stats ===")
        print(f"Rounds played: {rounds_played}")
        print(f"Rounds won:    {rounds_won}")
        print(f"Total score:   {total_score}\n")

        if not ask_play_again():
            break

    print("\nThanks for playing Number Quest!")
    print(f"Final score: {total_score}")


if __name__ == "__main__":
    main()
