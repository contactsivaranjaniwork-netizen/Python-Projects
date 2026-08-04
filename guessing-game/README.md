# 🎯 Number Guessing Game with Difficulty Levels

A command-line number guessing game where the computer picks a secret number in a range, and you try to find it within a limited number of guesses — with three difficulty levels and persisted per-difficulty best scores.

## Features

- **Three difficulty levels** — Easy (1–50, 10 guesses), Medium (1–100, 7 guesses), Hard (1–200, 5 guesses).
- **Higher/lower feedback** — after each guess, told whether to go higher or lower, with guesses remaining shown.
- **Smart input handling** — non-numeric or out-of-range guesses are rejected with a clear message and **don't cost a turn**.
- **Persisted stats** — games played, wins, losses, and your best (fewest-guesses) score are tracked per difficulty and saved to `guessing_stats.json`, carried across runs.
- Core game logic (range/limit lookup, guess comparison, input validation, stats updates) is fully separated from user input/output, so it's independently unit-tested.

## Demo

```
===== NUMBER GUESSING GAME =====
1. Play a Round
2. View Stats
3. Exit
=================================
Choose an option: 1
Choose difficulty:
1. Easy (1-50, 10 guesses)
2. Medium (1-100, 7 guesses)
3. Hard (1-200, 5 guesses)
Choice: 2

Guess a number between 1 and 100. You have 7 guesses.
Guess 1: 50
Too low!
Guesses remaining: 6
Guess 2: 75
Too high!
Guesses remaining: 5
Guess 3: 62
Correct! You won in 3 guess(es).
```

```
Choose an option: 2

Total games played: 1

Medium   | Played: 1   | Wins: 1   | Losses: 0   | Win rate: 100.0% | Best: 3
```

## Project Structure

```
number-guessing-game/
├── project.py             # main program (menu loop + game logic)
├── test_project.py         # pytest test suite
├── guessing_stats.json      # stats (created automatically)
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/contactsivaranjaniwork-netizen/Python-Projects.git
cd python-portfolio/guessing-game
pip install -r requirements.txt
```

## Usage

```bash
python3 project.py
```

Choose a difficulty, guess the number, and check your best scores anytime from the Stats menu.

## Running Tests

```bash
pytest test_project.py -v
```

The test suite covers:
- `get_difficulty_settings` returns the correct range/limit for each difficulty (case-insensitively) and raises `ValueError` for an unknown one
- `check_guess` correctly returns `"too_low"`, `"too_high"`, and `"correct"`
- `is_valid_guess` correctly parses valid input and raises `ValueError` for non-numeric, out-of-range, or non-integer input
- `update_stats` correctly tracks wins/losses per difficulty
- `update_stats` only replaces the best (fewest-guesses) score when a new result is **strictly** better — verified with a worse, better, and tied result in sequence
- Stats loading/saving round-trip correctly (using `pytest`'s `tmp_path`, so tests never touch your real `guessing_stats.json`), and corrupted files fall back to defaults
- `format_stats` produces the expected display text, including the "no games yet" case

## Design Notes

The program separates **pure logic** from **I/O**:

| Function | Responsibility |
|---|---|
| `get_difficulty_settings(difficulty)` | Pure — looks up range/guess-limit, validates the name |
| `check_guess(secret_number, guess)` | Pure — comparison logic |
| `is_valid_guess(guess_str, min_range, max_range)` | Pure — parses and validates input |
| `update_stats(stats, difficulty, won, guesses_used)` | Pure — updates counts and best score, only replacing on strict improvement |
| `load_stats(stats_file)` / `save_stats(...)` | I/O — JSON persistence with corrupted/missing-file handling |
| `format_stats(stats)` | Pure — formats stats into display text |
| `get_difficulty_choice()` / `play_round(...)` | I/O — menu prompts and the actual guessing loop |
| `main()` | Top-level menu loop |

This separation is what makes every scoring rule (including the "only update best score if strictly better" logic) directly testable without needing to simulate an entire game session.

## Possible Improvements

- A hint option that costs a guess but narrows the range
- A custom mode where the player sets their own range and guess limit
- A "hot/cold" indicator based on how close the last guess was
- A global leaderboard across difficulties ranked by fewest guesses

## License

Part of the [Python Project Portfolio](../README.md) — see the root [LICENSE](../LICENSE) file.
