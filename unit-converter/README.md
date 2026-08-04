# 🌡️ Unit Converter

A command-line tool for converting values between common units of **temperature**, **length**, and **weight**, with a simple menu-driven interface.

## Features

- **Temperature** — convert between Celsius, Fahrenheit, and Kelvin (all 6 directions), with validation against physically impossible values (below absolute zero).
- **Length** — convert between meters, kilometers, centimeters, millimeters, miles, feet, and inches.
- **Weight** — convert between kilograms, grams, pounds, and ounces.
- Menu loop lets you perform multiple conversions in one session.
- Invalid menu choices and non-numeric input are caught and re-prompted instead of crashing the program.
- Core conversion logic is fully separated from user input/output, so it's independently unit-tested.

## Demo

```
=====  UNIT CONVERTER =====
 1. Temperature Conversion
 2. Length Conversion
 3. Weight Conversion
======================
Enter your choice: 1

=====  Temperature Conversion  =====
 1. Celsius to Fahrenheit
 2. Fahrenheit to Celsius
 3. Celsius to Kelvin
 4. Kelvin to Celsius
 5. Fahrenheit to Kelvin
 6. Kelvin to Fahrenheit
======================
Choice: 1
Enter temp in C: 25
25.00 °C = 77.00 °F

Do you want another conversion? (y/n): n
Thank you for using the Converter!
```

## Project Structure

```
unit-converter/
├── Unit_Converter.py       # main program (menu loop + conversion logic)
├── test_Unit_Converter.py  # pytest test suite
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/contactsivaranjaniwork-netizen/Python-Projects.git
cd python-portfolio/unit-converter
pip install -r requirements.txt
```

## Usage

```bash
python3 Unit_Converter.py
```

Follow the on-screen menu to choose a conversion category, then a specific unit pair, and enter the value to convert.

## Running Tests

```bash
pytest test_Unit_Converter.py -v
```

The test suite covers:
- Correct conversion values across all three categories
- Rejection of temperatures below absolute zero
- Rejection of negative lengths/weights
- Rejection of unsupported/unknown units

## Design Notes

The program separates **pure logic** from **I/O**:

| Function | Responsibility |
|---|---|
| `convert_temperature(value, from_unit, to_unit)` | Pure conversion logic, no I/O |
| `convert_length(value, from_unit, to_unit)` | Pure conversion logic, no I/O |
| `convert_weight(value, from_unit, to_unit)` | Pure conversion logic, no I/O |
| `get_float(prompt)` | Input validation helper |
| `temperature_menu()` / `length_menu()` / `weight_menu()` | I/O wrappers around the conversion functions |
| `main()` | Top-level menu loop |

This separation is what makes the conversion functions testable directly with `pytest`, without needing to mock `input()`.

## Possible Improvements

- Support chaining conversions (convert the result again without re-entering the value)
- Add a `--batch` mode to read/write conversions via CSV
- Colorized CLI output (e.g., using `rich`)
