"""
Text-Based Hangman (CLI)
Classic word-guessing game with a word bank, limited guesses, and
ASCII art for lives remaining.

Structure:
- choose_word / get_display_word / process_guess / is_game_won / is_game_lost: pure, testable
- load_words / load_stats / save_stats: file I/O with corrupted/missing-file handling
- play_round / main: I/O, uses process_guess's returned status to decide what to print
"""

import json
import os
import random

WORDS_FILE = "words.json"
STATS_FILE = "stats.json"
LIVES = 7

DEFAULT_WORD_BANK = {
    "General": {
        "Easy": ["apple", "banana", "grape", "house", "train"],
        "Hard": ["rhythm", "psychology", "luxury", "galaxy", "knight"],
    }
}

DEFAULT_STATS = {"games_played": 0, "wins": 0, "losses": 0}

HANGMAN = [
    r"""
  +---+
      |
      |
      |
      |
      |
=========
""",
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
""",
]


def load_words(word_file=WORDS_FILE):
    """
    Load the word bank from a JSON file. If the file doesn't exist, create
    it with a default word bank. If the file exists but is corrupted,
    return the default bank in memory without overwriting the file (so
    the user can inspect/fix it manually).
    """
    if not os.path.exists(word_file):
        with open(word_file, "w", encoding="utf-8") as file:
            json.dump(DEFAULT_WORD_BANK, file, indent=4)
        return dict(DEFAULT_WORD_BANK)

    try:
        with open(word_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return dict(DEFAULT_WORD_BANK)


def load_stats(stats_file=STATS_FILE):
    """
    Load game statistics from a JSON file, falling back to defaults if
    the file doesn't exist or is corrupted.
    """
    if not os.path.exists(stats_file):
        return dict(DEFAULT_STATS)

    try:
        with open(stats_file, "r", encoding="utf-8") as file:
            stats = json.load(file)
    except json.JSONDecodeError:
        return dict(DEFAULT_STATS)

    if not isinstance(stats, dict):
        return dict(DEFAULT_STATS)

    return stats


def save_stats(stats, stats_file=STATS_FILE):
    """Save game statistics to a JSON file."""
    with open(stats_file, "w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4)


def choose_word(word_bank, category=None, difficulty=None):
    """
    Pick a random word from the word bank, optionally filtered by
    category and/or difficulty. Falls back to a random category/
    difficulty if the requested one isn't specified or doesn't exist.
    """
    if not category or category not in word_bank:
        category = random.choice(list(word_bank.keys()))

    if not difficulty or difficulty not in word_bank[category]:
        difficulty = random.choice(list(word_bank[category].keys()))

    return random.choice(word_bank[category][difficulty])


def get_display_word(word, guessed_letters):
    """Return the word with unguessed letters replaced by underscores."""
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def process_guess(word, guess, guessed_letters, wrong_guesses):
    """
    Validate and apply a single letter guess, mutating guessed_letters/
    wrong_guesses in place as appropriate.

    Returns a status string: 'invalid', 'repeat', 'correct', or 'incorrect'.
    Does NOT print anything — callers decide what to display based on
    the returned status, which is what makes this testable without
    capturing stdout.
    """
    guess = guess.lower()

    if len(guess) != 1 or not guess.isalpha():
        return "invalid"

    if guess in guessed_letters or guess in wrong_guesses:
        return "repeat"

    if guess in word:
        guessed_letters.add(guess)
        return "correct"
    else:
        wrong_guesses.add(guess)
        return "incorrect"


def is_game_won(word, guessed_letters):
    """Return True if every letter in the word has been guessed."""
    return all(letter in guessed_letters for letter in word)


def is_game_lost(wrong_guesses, max_wrong=LIVES):
    """Return True if the number of wrong guesses has reached the limit."""
    return len(wrong_guesses) >= max_wrong


def play_round(word_bank, category, difficulty, stats, max_lives=LIVES, stats_file=STATS_FILE):
    """Run a single round of Hangman, updating and saving stats at the end."""
    word = choose_word(word_bank, category, difficulty).lower()
    guessed_letters = set()
    wrong_guesses = set()

    print("\n--- New Round ---")
    print(f"Category: {category or 'Random'} | Difficulty: {difficulty or 'Random'}")

    while True:
        print(HANGMAN[len(wrong_guesses)])
        print(f"Word: {get_display_word(word, guessed_letters)}")
        print(f"Wrong guesses: {', '.join(sorted(wrong_guesses)) or '(none)'}")
        print(f"Lives remaining: {max_lives - len(wrong_guesses)}")

        guess = input("Guess a letter: ").strip()
        status = process_guess(word, guess, guessed_letters, wrong_guesses)

        if status == "invalid":
            print("Please enter a single valid letter.")
        elif status == "repeat":
            print("You already guessed that letter!")
        elif status == "correct":
            print("Correct!")
        elif status == "incorrect":
            print("Incorrect!")

        if is_game_won(word, guessed_letters):
            print(f"\nCongratulations! You won! The word was: {word}")
            stats["games_played"] += 1
            stats["wins"] += 1
            save_stats(stats, stats_file)
            return

        if is_game_lost(wrong_guesses, max_lives):
            print(HANGMAN[len(wrong_guesses)])
            print(f"\nGame Over! You ran out of lives. The word was: {word}")
            stats["games_played"] += 1
            stats["losses"] += 1
            save_stats(stats, stats_file)
            return


def main():
    word_bank = load_words()
    stats = load_stats()

    current_category = None
    current_difficulty = None

    while True:
        print(
            "\n===== HANGMAN =====\n"
            "1. Play a Round\n"
            "2. Choose Category / Difficulty\n"
            "3. View Stats\n"
            "4. Exit\n"
            "=============================="
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            play_round(word_bank, current_category, current_difficulty, stats)

        elif choice == "2":
            print("\nAvailable Categories:")
            categories = list(word_bank.keys())
            for idx, cat in enumerate(categories, 1):
                print(f"{idx}. {cat}")

            cat_choice = input("Select category number (or press Enter for random): ")
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
                current_category = categories[int(cat_choice) - 1]

                print("\nAvailable Difficulties:")
                diffs = list(word_bank[current_category].keys())
                for idx, diff in enumerate(diffs, 1):
                    print(f"{idx}. {diff}")
                diff_choice = input("Select difficulty number (or press Enter for random): ")
                if diff_choice.isdigit() and 1 <= int(diff_choice) <= len(diffs):
                    current_difficulty = diffs[int(diff_choice) - 1]
                else:
                    current_difficulty = None
            else:
                current_category = None
                current_difficulty = None
                print("Set to completely random word.")

        elif choice == "3":
            print("\n===== STATISTICS =====")
            print(f"Games Played: {stats['games_played']}")
            print(f"Wins: {stats['wins']}")
            print(f"Losses: {stats['losses']}")
            win_rate = (stats["wins"] / stats["games_played"] * 100) if stats["games_played"] > 0 else 0
            print(f"Win Rate: {win_rate:.1f}%")
            print("======================")

        elif choice == "4":
            print("Thanks for playing!")
            break

        else:
            print("Invalid choice. Please choose from the given menu")


if __name__ == "__main__":
    main()
    