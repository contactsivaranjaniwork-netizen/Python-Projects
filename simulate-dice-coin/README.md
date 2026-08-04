# 🎲 Dice Roller / Coin Flip Simulator

A command-line tool that simulates dice rolls and coin flips, tracking running statistics — like per-face dice counts and heads/tails ratios — across a session.

## Features

- **Roll dice** — choose any number of dice and any number of sides per die; see individual results and the total.
- **Flip coins** — flip any number of coins at once and see the full sequence of results.
- **Live statistics** — view running counts and percentages for every dice face rolled and for heads/tails, updated after every action.
- **Reset with confirmation** — clear all tracked statistics, with a confirmation prompt to avoid accidental resets.
- Invalid input (non-numbers, zero/negative counts, single-sided dice) re-prompts in place instead of bouncing back to the main menu or crashing.
- Core statistics logic is fully separated from user input/output, so it's independently unit-tested.

## Demo

```
===== DICE ROLLER / COIN FLIP SIMULATOR =====
1. Roll a Die
2. Flip a Coin
3. View Statistics
4. Reset Statistics
5. Exit
==============================================
Enter your choice: 1
How many dice? 2
How many sides per die? 6
Rolls: [4, 6]  Total: 10

Enter your choice: 3

--- Dice Statistics ---
Total Rolls: 2

Side 4: 1 (50.0%)
Side 6: 1 (50.0%)

--- Coin Statistics ---
No coin flips yet.
```

## Project Structure

```
dice-coin-simulator/
├── project.py        # main program (menu loop + stats logic)
├── test_project.py    # pytest test suite
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/contactsivaranjaniwork-netizen/Python-Projects.git
cd python-portfolio/simulate-dice-coin
pip install -r requirements.txt
```

## Usage

```bash
python3 project.py
```

Choose to roll dice, flip coins, view accumulated statistics, or reset everything back to zero.

## Running Tests

```bash
pytest test_project.py -v
```

The test suite covers:
- `roll_dice` returns the correct number of results, all within `[1, sides]`
- `flip_coins` returns only `"Heads"`/`"Tails"` results
- Invalid dice count/sides/flip count raise `ValueError`
- `update_stats` correctly accumulates counts across multiple calls
- `get_stats_summary` computes correct totals and percentages, including the empty-stats case
- `format_dice_summary`/`format_coin_summary` produce the expected display text
- `reset_stats` clears multiple stats dicts at once

## Design Notes

The program separates **pure logic** from **I/O**:

| Function | Responsibility |
|---|---|
| `roll_dice(num_dice, sides)` | Pure — random dice results, validates inputs |
| `flip_coins(num_flips)` | Pure — random coin results, validates inputs |
| `update_stats(stats, results)` | Pure — accumulates running counts |
| `get_stats_summary(stats)` | Pure — computes totals and percentages |
| `format_dice_summary(stats)` / `format_coin_summary(stats)` | Pure — formats stats as display text |
| `reset_stats(*stats_dicts)` | Pure — clears any number of stats dicts |
| `get_positive_int(prompt, minimum)` | Input validation helper |
| `main()` | Top-level menu loop |

This separation is what makes every statistics function directly testable with `pytest`, without needing to capture or mock printed output.

## Possible Improvements

- Persist statistics across sessions in a JSON file
- Add a "weighted"/loaded die or coin mode for exploring probability concepts
- Show a text-based bar chart (`█████`) per face/side instead of just numbers
- Support dice notation like `2d6+3`

## License

Part of the [Python Project Portfolio](../README.md) — see the root [LICENSE](../LICENSE) file.
