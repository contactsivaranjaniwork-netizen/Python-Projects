# ⚖️ BMI & Calorie Calculator

A command-line tool that calculates Body Mass Index (BMI), classifies it into a standard health category, and estimates daily calorie needs based on age, sex, weight, height, and activity level.

## Features

- **BMI calculation** — computes BMI from weight (kg) and height (cm) using the standard formula.
- **Health classification** — categorizes BMI into Underweight, Normal weight, Overweight, or Obese, with correct boundary handling (18.5, 25, and 30 are inclusive of the higher category).
- **Calorie needs estimation** — calculates Basal Metabolic Rate (BMR) via the Mifflin-St Jeor equation, then applies an activity multiplier (Sedentary → Very Active) to estimate daily maintenance calories.
- **Combined mode** — run both calculations from a single set of inputs, no re-entry required.
- All numeric and categorical input (weight, height, age, sex, activity level) is validated and re-prompted on invalid entry instead of crashing.
- Core formulas are fully separated from user input/output, so they're independently unit-tested.

## Demo

```
===== BMI & CALORIE CALCULATOR =====
1. Calculate BMI
2. Calculate Daily Calorie Needs
3. Calculate Both
4. Exit
=====================================
Choose an option: 1
Enter your weight (kg): 70
Enter your height (cm): 175

Your BMI is 22.9 — Normal weight
```

```
Choose an option: 2
Enter your age: 30
Enter your sex (M/F): M
Enter your weight (kg): 70
Enter your height (cm): 175
Select activity level:
 1. Sedentary
 2. Lightly Active
 3. Moderately Active
 4. Very Active
Choice: 3

Estimated daily calorie needs: 2556 kcal
```

## Project Structure

```
bmi-calorie-calculator/
├── project.py        # main program (menu loop + formulas)
├── test_project.py    # pytest test suite
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/contactsivaranjaniwork-netizen/Python-Projects.git
cd python-portfolio/BMI-calculator
pip install -r requirements.txt
```

## Usage

```bash
python3 project.py
```

Choose to calculate BMI, calorie needs, or both — enter your details when prompted.

## Running Tests

```bash
pytest test_project.py -v
```

The test suite covers:
- Correct BMI calculation for known weight/height pairs
- Correct classification at every category boundary (18.5, 25, 30) and within each range
- Correct BMR calculation for both sexes (Mifflin-St Jeor formula)
- Correct calorie estimates across all four activity levels
- Invalid input (non-positive weight/height/age, invalid sex, invalid activity level) raising `ValueError`

## Design Notes

The program separates **pure logic** from **I/O**:

| Function | Responsibility |
|---|---|
| `calculate_bmi(weight_kg, height_cm)` | Pure — BMI formula, validates inputs |
| `classify_bmi(bmi)` | Pure — category classification, validates input |
| `calculate_bmr(weight_kg, height_cm, age, sex)` | Pure — Mifflin-St Jeor BMR, validates inputs |
| `calculate_daily_calories(bmr, activity_level)` | Pure — applies activity multiplier, validates level |
| `get_positive_float` / `get_positive_int` / `get_sex` / `get_activity_level` | Input validation helpers |
| `get_weight_and_height()` / `get_full_profile()` | Shared prompt sequences, avoiding duplication across menu options |
| `main()` | Top-level menu loop |

This separation is what makes all four calculation functions directly testable with `pytest`, and avoids the prompt duplication that existed across the original "Calculate BMI" / "Calculate Calories" / "Calculate Both" branches.

## Possible Improvements

- Support imperial units (feet/inches, pounds) as an alternative input mode
- Show a text-based BMI scale/gauge in the terminal
- Suggest a healthy weight range for the user's height
- Log calculation history to a file, similar to the calculator project
- Add a body fat percentage estimate (e.g., U.S. Navy method)

## License

Part of the [Python Project Portfolio](../README.md) — see the root [LICENSE](../LICENSE) file.
