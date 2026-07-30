# ⏱️ Countdown Timer / Pomodoro Clock

A command-line Pomodoro timer that runs work/break intervals with a live countdown display, plays a sound alert at the end of each interval, tracks session history, and lets you customize durations via persisted settings.

## Features

- **Pomodoro sessions** — runs a configurable number of work sessions, automatically alternating short breaks and long breaks (a long break every N work sessions, per your settings).
- **Custom timer** — a one-off work + break countdown with arbitrary durations, without the full Pomodoro cycle structure.
- **Live countdown display** — updates every second in place (`MM:SS`) in the terminal.
- **Sound alert** — plays the terminal bell (`\a`) when each interval ends, along with a clear text announcement.
- **Session history** — every completed interval is logged to `pomodoro_history.csv` with a timestamp; view a daily summary of work sessions completed and minutes focused.
- **Persisted settings** — customize work duration, short/long break duration, and how many work sessions occur before a long break — saved to `pomodoro_settings.json` and reused on the next run.
- **Safe interruption** — pressing Ctrl+C during any interval stops that session early and returns cleanly to the main menu, without exiting the whole program.

## Demo

```
===== POMODORO CLOCK =====
1. Start a Pomodoro Session
2. Custom Timer
3. View Session History
4. Settings
5. Exit
==============================
Choose an option: 1
How many work sessions do you want to complete? 2

--- Starting Work Session 1 (25 min) ---
Press Ctrl+C to stop this session early.
Work Session 1 — Time remaining: 24:59
...
Work Session 1 — Time remaining: 00:00
Work Session 1 complete!

--- Starting Short Break (5 min) ---
...
```

## Project Structure

```
pomodoro-clock/
├── project.py               # main program (menu loop + timer/settings logic)
├── test_project.py           # pytest test suite
├── pomodoro_history.csv       # session log (created automatically)
├── pomodoro_settings.json     # persisted settings (created automatically)
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/<your-username>/python-portfolio.git
cd python-portfolio/pomodoro-clock
pip install -r requirements.txt
```

## Usage

```bash
python3 project.py
```

Start a Pomodoro session, run a one-off custom timer, view your history, or adjust your work/break durations in Settings.

## Running Tests

```bash
pytest test_project.py -v
```

The test suite covers:
- `format_time` converts seconds to `MM:SS` correctly, including durations over an hour
- `build_pomodoro_sequence` produces the correct interval order and count, with the long break landing in the right position
- Invalid sequence parameters (zero cycles, non-positive durations) raise `ValueError`
- Session logging and history reading round-trip correctly (using `pytest`'s `tmp_path`, so tests never touch your real history file)
- `get_session_summary` correctly aggregates totals for a given date and filters out other days/types
- Settings load/save round-trip correctly, and fall back to defaults on a missing or corrupted config file

Note: none of these tests involve waiting through real countdowns — the sequence-building logic is fully separated from `time.sleep()`, so tests run in milliseconds.

## Design Notes

The program separates **sequence planning** from **execution**, and **logic** from **I/O**:

| Function | Responsibility |
|---|---|
| `format_time(seconds)` | Pure — MM:SS formatting |
| `build_pomodoro_sequence(...)` | Pure — plans the full interval list, no `time.sleep` |
| `run_countdown(duration_min, label)` | I/O — the actual live countdown + bell |
| `run_sequence(sequence, log_file)` | I/O — runs and logs each planned interval in order |
| `log_session(...)` / `read_history(...)` | I/O — CSV history persistence |
| `get_session_summary(history, date_str, session_type)` | Pure — aggregates history into stats |
| `format_summary(count, total_minutes)` | Pure — formats stats as display text |
| `load_settings(...)` / `save_settings(...)` | I/O — JSON settings persistence, with defaults fallback |
| `get_positive_int(prompt, minimum, maximum)` | Input validation helper |
| `main()` | Top-level menu loop |

### Why this matters: the early-exit bug

An earlier version had a `break` statement inside the Custom Timer branch that accidentally broke out of `main()`'s top-level menu loop instead of just stopping the current timer — so pressing Ctrl+C during a custom session would silently exit the *entire program*, not just return to the menu. The fix wasn't just moving the `break` — it was restructuring so that **`main()` never needs a `break` for this at all**: `run_sequence()` simply returns `True`/`False` and control naturally falls back to the menu loop afterward, regardless of which menu option was running. This makes the bug structurally impossible to reintroduce.

## Possible Improvements

- Desktop notifications (e.g., via `plyer`) in addition to the terminal bell
- A visual progress bar during the countdown instead of just `MM:SS` text
- Pause/resume support for an in-progress interval
- Export session history to a summary chart or CSV report for a date range
- A `--minutes N` CLI flag to instantly start a custom timer without the menu

## License

Part of the [Python Project Portfolio](../README.md) — see the root [LICENSE](../LICENSE) file.
