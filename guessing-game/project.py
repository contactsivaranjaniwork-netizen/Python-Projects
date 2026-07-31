"""
Number Guessing Game with Difficulty Levels (CLI)
Computer picks a number in a range; difficulty changes the range size
and guess limit.

Structure:
- get_difficulty_settings / check_guess / is_valid_guess / update_stats: pure, testable
- load_stats / save_stats / format_stats: history I/O and formatting
- play_round / main: I/O, uses the pure functions above
"""

import json
import os
import random

STATS_FILE = "guessing_stats.json"

# difficulty -> (min_range, max_range, max_guesses)
DIFFICULTY_SETTINGS = {
    "easy": (1, 50, 10),
    "medium": (1, 100, 7),
    "hard": (1, 200, 5),
}

DEFAULT_STATS = {"games_played": 0, "difficulties": {}}


def get_difficulty_settings(difficulty):
    """
    Return (min_range, max_range, max_guesses) for a difficulty name
    ('easy', 'medium', 'hard' — case-insensitive).
    Raises ValueError for an unknown difficulty.
    """
    key = difficulty.lower()
    if key not in DIFFICULTY_SETTINGS:
        raise ValueError(f"Unknown difficulty: {difficulty}")
    return DIFFICULTY_SETTINGS[key]


def check_guess(secret_number, guess):
    """Return 'correct', 'too_high', or 'too_low' comparing guess to secret_number."""
    if guess < secret_number:
        return "too_low"
    elif guess > secret_number:
        return "too_high"
    else:
        return "correct"


def is_valid_guess(guess_str, min_range, max_range):
    """
    Parse and validate a guess string.
    Returns the parsed int if valid.
    Raises ValueError if it's not a whole number or is outside [min_range, max_range].
    """
    try:
        guess = int(guess_str)
    except ValueError:
        raise ValueError("Guess must be a whole number")

    if guess < min_range or guess > max_range:
        raise ValueError(f"Guess must be between {min_range} and {max_range}")

    return guess


def update_stats(stats, difficulty, won, guesses_used):
    """
    Update the stats dict in place for a completed round, tracking
    games played, wins, losses, and best (fewest-guesses) score per
    difficulty — only replacing the best score when strictly better.
    Returns the same stats dict for convenience/chaining.
    """
    difficulty = difficulty.lower()

    if difficulty not in stats["difficulties"]:
        stats["difficulties"][difficulty] = {
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "best_guesses": None,
        }

    entry = stats["difficulties"][difficulty]
    entry["games_played"] += 1
    stats["games_played"] += 1

    if won:
        entry["wins"] += 1
        if entry["best_guesses"] is None or guesses_used < entry["best_guesses"]:
            entry["best_guesses"] = guesses_used
    else:
        entry["losses"] += 1

    return stats


def load_stats(stats_file=STATS_FILE):
    """
    Load stats from a JSON file, falling back to defaults if the file
    doesn't exist or is corrupted.
    """
    if not os.path.exists(stats_file):
        return {"games_played": 0, "difficulties": {}}

    try:
        with open(stats_file, "r", encoding="utf-8") as file:
            stats = json.load(file)
    except json.JSONDecodeError:
        return {"games_played": 0, "difficulties": {}}

    if not isinstance(stats, dict) or "difficulties" not in stats:
        return {"games_played": 0, "difficulties": {}}

    return stats


def save_stats(stats, stats_file=STATS_FILE):
    """Save stats to a JSON file."""
    with open(stats_file, "w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4)


def format_stats(stats):
    """Return a formatted multi-line string summarizing stats across all difficulties."""
    if stats["games_played"] == 0:
        return "No games played yet."

    lines = [f"Total games played: {stats['games_played']}", ""]
    for difficulty, entry in sorted(stats["difficulties"].items()):
        win_rate = (entry["wins"] / entry["games_played"] * 100) if entry["games_played"] else 0
        best = entry["best_guesses"] if entry["best_guesses"] is not None else "—"
        lines.append(
            f"{difficulty.capitalize():<8} | Played: {entry['games_played']:<3} | "
            f"Wins: {entry['wins']:<3} | Losses: {entry['losses']:<3} | "
            f"Win rate: {win_rate:5.1f}% | Best: {best}"
        )
    return "\n".join(lines)


def get_difficulty_choice():
    """Prompt for and return a valid difficulty name."""
    difficulties = list(DIFFICULTY_SETTINGS.keys())
    print("Choose difficulty:")
    for idx, name in enumerate(difficulties, 1):
        min_r, max_r, max_g = DIFFICULTY_SETTINGS[name]
        print(f"{idx}. {name.capitalize()} ({min_r}-{max_r}, {max_g} guesses)")

    while True:
        choice = input("Choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(difficulties):
            return difficulties[int(choice) - 1]
        print(f"Please enter a number from 1 to {len(difficulties)}.")


def play_round(difficulty, stats, stats_file=STATS_FILE):
    """Run a single round of the guessing game, updating and saving stats at the end."""
    min_range, max_range, max_guesses = get_difficulty_settings(difficulty)
    secret_number = random.randint(min_range, max_range)

    print(f"\nGuess a number between {min_range} and {max_range}. You have {max_guesses} guesses.")

    guesses_used = 0
    while guesses_used < max_guesses:
        guess_str = input(f"Guess {guesses_used + 1}: ")

        try:
            guess = is_valid_guess(guess_str, min_range, max_range)
        except ValueError as e:
            print(f"Invalid guess: {e}")
            continue  # doesn't consume a turn

        guesses_used += 1
        result = check_guess(secret_number, guess)

        if result == "correct":
            print(f"Correct! You won in {guesses_used} guess(es).")
            update_stats(stats, difficulty, won=True, guesses_used=guesses_used)
            save_stats(stats, stats_file)
            return
        elif result == "too_low":
            print("Too low!")
        else:
            print("Too high!")

        remaining = max_guesses - guesses_used
        if remaining > 0:
            print(f"Guesses remaining: {remaining}")

    print(f"\nOut of guesses! The number was {secret_number}.")
    update_stats(stats, difficulty, won=False, guesses_used=guesses_used)
    save_stats(stats, stats_file)


def main():
    stats = load_stats()

    while True:
        print(
            "\n===== NUMBER GUESSING GAME =====\n"
            "1. Play a Round\n"
            "2. View Stats\n"
            "3. Exit\n"
            "================================="
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            difficulty = get_difficulty_choice()
            play_round(difficulty, stats)

        elif choice == "2":
            print(f"\n{format_stats(stats)}")

        elif choice == "3":
            print("Thanks for playing!")
            break

        else:
            print("Invalid choice. Please choose from the given menu.")


if __name__ == "__main__":
    main()