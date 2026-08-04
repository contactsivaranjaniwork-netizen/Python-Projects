# 🧮 Simple Calculator with History

A command-line calculator supporting seven arithmetic operations, with every calculation automatically logged to a timestamped history file.

## Features

- **Seven operations** — addition, subtraction, multiplication, division, modulus, exponent, and floor division.
- **Decimal support** — accepts both integers and floating-point numbers.
- **Calculation history** — every successful calculation is appended to `history.txt` with a timestamp, and can be viewed from the menu at any time.
- **Safe error handling** — division/modulus/floor-division by zero, and undefined cases like `0 ** -1`, are caught and reported cleanly instead of crashing.
- Core arithmetic logic is fully separated from user input/output, so it's independently unit-tested.

## Demo

```
===== CALCULATOR =====
 1. Addition
 2. Subtraction
 3. Multiplication
 4. Division
 5. Modulus
 6. Exponent
 7. Floor Division
 8. View History
 9. Exit
======================
Enter your choice: 1
Enter the first number: 5
Enter the second number: 3
5.0 + 3.0 = 8.0

Do you want another calculation? (y/n): n
Thank you for using the calculator!
```

Viewing history:
```
Enter your choice: 8

--- Calculation History ---
[2026-07-27 09:51:20] 5.0 + 3.0 = 8.0
----------------------------
```

## Project Structure

```
calculator/
├── project.py        # main program (menu loop + arithmetic logic)
├── test_project.py    # pytest test suite
├── history.txt        # generated automatically on first calculation
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/contactsivaranjaniwork-netizen/Python-Projects.git
cd python-portfolio/calculator-with-memory
pip install -r requirements.txt
```

## Usage

```bash
python3 project.py
```

Pick an operation, enter two numbers, and the result is calculated and logged automatically. Choose option 8 anytime to review past calculations.

## Running Tests

```bash
pytest test_project.py -v
```

The test suite covers:
- All seven operations, with both integer and float inputs
- Division, modulus, and floor-division by zero raising `ZeroDivisionError`
- The `0 ** -1` undefined-exponent edge case
- An unsupported operation raising `ValueError`
- Expression formatting output
- Writing to and reading back from a history file (using `pytest`'s `tmp_path` fixture, so tests never touch your real history file)

## Design Notes

The program separates **pure logic** from **I/O**:

| Function | Responsibility |
|---|---|
| `calculate(a, b, operation)` | Pure — performs the arithmetic, raises on invalid cases |
| `format_expression(a, b, symbol, result)` | Pure — formats a calculation as a display string |
| `log_calculation(expression, filepath)` | I/O — appends a timestamped line to the history file |
| `read_history(filepath)` | I/O — reads back past calculations |
| `get_number(prompt)` | Input validation helper |
| `main()` | Top-level menu loop |

This separation is what makes `calculate` and `format_expression` directly testable with `pytest`, and lets `log_calculation`/`read_history` be tested against a temporary file instead of your real history.

## Possible Improvements

- Add a "clear history" menu option
- Support chained calculations (use the last result as the next first number)
- Add square root / other unary operations
- Export history to CSV for use in a spreadsheet

## License

Part of the [Python Project Portfolio](../README.md) — see the root [LICENSE](../LICENSE) file.
