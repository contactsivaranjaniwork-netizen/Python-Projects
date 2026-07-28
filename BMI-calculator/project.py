"""
BMI & Calorie Calculator (CLI)
Takes height and weight input, computes BMI, and classifies the result
into a health category. Also estimates daily calorie needs via BMR.

Structure:
- calculate_bmi / classify_bmi / calculate_bmr / calculate_daily_calories: pure, testable
- get_*: input validation helpers
- main: top-level menu loop
"""

ACTIVITY_MULTIPLIERS = {
    "1": 1.2,    # Sedentary
    "2": 1.375,  # Lightly Active
    "3": 1.55,   # Moderately Active
    "4": 1.725,  # Very Active
}


def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI given weight in kilograms and height in centimeters.
    Raises ValueError if weight or height is not positive.
    """
    if weight_kg <= 0:
        raise ValueError("Weight must be a positive number")
    if height_cm <= 0:
        raise ValueError("Height must be a positive number")

    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)


def classify_bmi(bmi):
    """
    Classify a BMI value into a standard health category.
    Raises ValueError if bmi is not positive.
    """
    if bmi <= 0:
        raise ValueError("BMI must be a positive number")

    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_bmr(weight_kg, height_cm, age, sex):
    """
    Calculate Basal Metabolic Rate using the Mifflin-St Jeor equation.
    sex must be 'm' or 'f' (case-insensitive).
    Raises ValueError for invalid weight, height, age, or sex.
    """
    if weight_kg <= 0:
        raise ValueError("Weight must be a positive number")
    if height_cm <= 0:
        raise ValueError("Height must be a positive number")
    if age <= 0:
        raise ValueError("Age must be a positive number")

    sex = sex.lower()
    if sex == "m":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif sex == "f":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        raise ValueError("Sex must be 'M' or 'F'")


def calculate_daily_calories(bmr, activity_level):
    """
    Estimate daily maintenance calories given a BMR and an activity level
    ('1' Sedentary, '2' Lightly Active, '3' Moderately Active, '4' Very Active).
    Raises ValueError for an unsupported activity level.
    """
    if activity_level not in ACTIVITY_MULTIPLIERS:
        raise ValueError("Activity level must be '1', '2', '3', or '4'")

    return bmr * ACTIVITY_MULTIPLIERS[activity_level]


def get_positive_float(prompt):
    """Repeatedly prompt until the user enters a positive float."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_positive_int(prompt):
    """Repeatedly prompt until the user enters a positive int."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_sex(prompt):
    """Repeatedly prompt until the user enters 'M' or 'F' (case-insensitive)."""
    while True:
        value = input(prompt).strip().lower()
        if value in ("m", "f"):
            return value
        print("Please enter 'M' or 'F'.")


def get_activity_level(prompt):
    """Repeatedly prompt until the user selects a valid activity level (1-4)."""
    while True:
        value = input(prompt).strip()
        if value in ACTIVITY_MULTIPLIERS:
            return value
        print("Please enter a number from 1 to 4.")


def get_weight_and_height():
    """Prompt for and return (weight_kg, height_cm)."""
    weight = get_positive_float("Enter your weight (kg): ")
    height = get_positive_float("Enter your height (cm): ")
    return weight, height


def get_full_profile():
    """Prompt for and return (age, sex, weight_kg, height_cm, activity_level)."""
    age = get_positive_int("Enter your age: ")
    sex = get_sex("Enter your sex (M/F): ")
    weight, height = get_weight_and_height()
    activity_level = get_activity_level(
        "Select activity level:\n"
        " 1. Sedentary\n"
        " 2. Lightly Active\n"
        " 3. Moderately Active\n"
        " 4. Very Active\n"
        "Choice: "
    )
    return age, sex, weight, height, activity_level


def print_bmi_result(weight, height):
    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)
    print(f"\nYour BMI is {bmi:.1f} — {category}")


def print_calorie_result(weight, height, age, sex, activity_level):
    bmr = calculate_bmr(weight, height, age, sex)
    calories = calculate_daily_calories(bmr, activity_level)
    print(f"\nEstimated daily calorie needs: {calories:.0f} kcal")


def main():
    while True:
        print(
            "\n===== BMI & CALORIE CALCULATOR =====\n"
            "1. Calculate BMI\n"
            "2. Calculate Daily Calorie Needs\n"
            "3. Calculate Both\n"
            "4. Exit\n"
            "====================================="
        )
        choice = input("Choose an option: ")

        if choice == "1":
            weight, height = get_weight_and_height()
            print_bmi_result(weight, height)

        elif choice == "2":
            age, sex, weight, height, activity_level = get_full_profile()
            print_calorie_result(weight, height, age, sex, activity_level)

        elif choice == "3":
            age, sex, weight, height, activity_level = get_full_profile()
            print_bmi_result(weight, height)
            print_calorie_result(weight, height, age, sex, activity_level)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()