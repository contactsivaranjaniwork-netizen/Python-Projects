# 🎯 Text-Based Hangman

A command-line Hangman game with a JSON-backed word bank organized by category and difficulty, progressive ASCII art as lives are lost, and persisted win/loss statistics.

## Features

- **Category & difficulty selection** — choose a category (e.g., General) and difficulty (Easy/Hard), or let the game pick randomly.
- **Classic gameplay** — guess letters one at a time; the word display updates in place as correct letters are revealed.
- **7 lives, 8-stage ASCII art** — a full hangman figure builds up one stage per wrong guess.
- **Smart input handling** — repeated guesses are rejected without costing a life; non-letter, multi-character, or empty input is rejected without crashing or consuming a turn.
- **Persisted stats** — games played, wins, losses, and win rate are saved to `stats.json` and carried across runs.
- **Persisted word bank** — stored in `words.json`, auto-created with sensible defaults on first run; you can add your own categories/words by editing the file directly.
- Core game logic (guess validation, win/loss detection, word masking) is fully separated from user input/output, so it's independently unit-tested.

## Demo

```
===== HANGMAN =====
1. Play a Round
2. Choose Category / Difficulty
3. View Stats
4. Exit
==============================
Choose an option: 1

--- New Round ---
Category: Random | Difficulty: Random

  +---+
      |
      |
      |
      |
      |
=========
Word: _ _ _ _ _
Wrong guesses: (none)
Lives remaining: 7
Guess a letter: p
Correct!
```

## Project Structure

```
hangman/
├── project.py         # main program (menu loop + game logic)
├── test_project.py     # pytest test suite
├── words.json           # word bank (created automatically with defaults)
├── stats.json            # win/loss stats (created automatically)
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/<your-username>/python-portfolio.git
cd python-portfolio/hangman
pip install -r requirements.txt
```

## Usage

```bash
python3 project.py
```

Play a round, pick a category/difficulty, check your stats, or add your own words by editing `words.json` (see its structure below).

### Word bank format

```json
{
    "Animals": {
        "Easy": ["cat", "dog"],
        "Hard": ["elephant", "kangaroo"]
    },
    "Movies": {
        "Easy": ["jaws", "cars"],
        "Hard": ["inception", "gladiator"]
    }
}
```

## Running Tests

```bash
pytest test_project.py -v
```

The test suite covers:
- `choose_word` respects a requested category/difficulty, and falls back gracefully for an invalid one
- `get_display_word` correctly masks/reveals letters for various guessed-letter sets
- `process_guess` correctly handles correct guesses, incorrect guesses, repeated guesses, and invalid input (non-letters, multi-character, empty) — all without printing anything, so no stdout capturing is needed
- `is_game_won` / `is_game_lost` at the exact boundary (last letter revealed → win; max wrong guesses reached → loss)
- Stats and word-bank loading/saving round-trip correctly (using `pytest`'s `tmp_path`, so tests never touch your real `stats.json`/`words.json`)
- Corrupted `stats.json`/`words.json` files fall back to defaults instead of crashing

## Design Notes

The program separates **pure logic** from **I/O**:

| Function | Responsibility |
|---|---|
| `choose_word(word_bank, category, difficulty)` | Pure — random selection with fallback |
| `get_display_word(word, guessed_letters)` | Pure — masks unguessed letters |
| `process_guess(word, guess, guessed_letters, wrong_guesses)` | Pure — validates/applies a guess, **returns a status string** (`invalid`/`repeat`/`correct`/`incorrect`) instead of printing |
| `is_game_won(word, guessed_letters)` | Pure — win check |
| `is_game_lost(wrong_guesses, max_wrong)` | Pure — loss check |
| `load_words(word_file)` / `load_stats(stats_file)` / `save_stats(...)` | I/O — JSON persistence, with corrupted/missing-file handling |
| `play_round(...)` | I/O — runs a round, prints based on `process_guess`'s returned status |
| `main()` | Top-level menu loop |

### Why `process_guess` returns a status instead of printing

An earlier version had `process_guess` print its own feedback messages directly, which meant its return value was never actually used by the caller — and there was no way to test "did this guess get treated as correct/incorrect/repeat/invalid" without capturing stdout. Now it returns one of four status strings and mutates `guessed_letters`/`wrong_guesses` in place; `play_round` decides what to display based on that status. This is what makes the guess-handling logic directly assertable in tests (`assert process_guess(...) == "correct"`).

## Possible Improvements

- Add a hint system (reveal one letter at the cost of a life)
- Two-player mode where one player sets the secret word
- A per-guess timer for a harder challenge mode
- Colorized correct/incorrect feedback (`rich` or ANSI codes)

## License

Part of the [Python Project Portfolio](../README.md) — see the root [LICENSE](../LICENSE) file.
