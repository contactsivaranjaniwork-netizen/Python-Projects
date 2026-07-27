"""
Simple Calculator with History (CLI)
Performs basic arithmetic and logs every calculation with a timestamp to a text file.

Structure:
- calculate: pure, testable arithmetic logic
- log_calculation / read_history: file I/O
- main: top-level menu loop
"""

from datetime import datetime

HISTORY_FILE = "history.txt"

# Maps menu choice -> (operation key, display symbol)
OPERATIONS = {
    "1": ("add", "+"),
    "2": ("subtract", "-"),
    "3": ("multiply", "*"),
    "4": ("divide", "/"),
    "5": ("modulus", "%"),
    "6": ("exponent", "**"),
    "7": ("floor_divide", "//"),
}


def calculate(a, b, operation):
    """
    Perform a basic arithmetic operation on a and b.
    operation must be one of: 'add', 'subtract', 'multiply', 'divide',
    'modulus', 'exponent', 'floor_divide'.
    Raises ValueError for an unsupported operation.
    Raises ZeroDivisionError for divide/modulus/floor_divide by zero,
    and for invalid zero-base exponents (e.g. 0 ** -1).
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ZeroDivisionError(f"Cannot divide {a} by {b}")
        return a / b
    elif operation == "modulus":
        if b == 0:
            raise ZeroDivisionError(f"Cannot divide {a} by {b}")
        return a % b
    elif operation == "exponent":
        try:
            return a ** b
        except ZeroDivisionError:
            raise ZeroDivisionError(f"{a} ** {b} is undefined")
    elif operation == "floor_divide":
        if b == 0:
            raise ZeroDivisionError(f"Cannot divide {a} by {b}")
        return a // b
    else:
        raise ValueError(f"Unsupported operation: {operation}")


def format_expression(a, b, symbol, result):
    """Format a calculation as a human-readable expression string."""
    return f"{a} {symbol} {b} = {result}"


def log_calculation(expression, filepath=HISTORY_FILE):
    """Append a timestamped calculation line to the history file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {expression}\n")


def read_history(filepath=HISTORY_FILE):
    """
    Return a list of past calculation log lines.
    Returns an empty list if the history file doesn't exist yet.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return [line.rstrip("\n") for line in file]
    except FileNotFoundError:
        return []


def get_number(prompt):
    """Repeatedly prompt until the user enters a valid number (int or float)."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def main():
    while True:
        print(
            "===== CALCULATOR =====\n"
            " 1. Addition\n"
            " 2. Subtraction\n"
            " 3. Multiplication\n"
            " 4. Division\n"
            " 5. Modulus\n"
            " 6. Exponent\n"
            " 7. Floor Division\n"
            " 8. View History\n"
            " 9. Exit\n"
            "======================"
        )
        choice = input("Enter your choice: ")

        if choice in OPERATIONS:
            operation, symbol = OPERATIONS[choice]
            a = get_number("Enter the first number: ")
            b = get_number("Enter the second number: ")
            try:
                result = calculate(a, b, operation)
                expression = format_expression(a, b, symbol, result)
                print(expression)
                log_calculation(expression)
            except ZeroDivisionError as e:
                print(f"Error: {e}")

        elif choice == "8":
            history = read_history()
            if not history:
                print("No calculations logged yet.")
            else:
                print("\n--- Calculation History ---")
                for line in history:
                    print(line)
                print("----------------------------")

        elif choice == "9":
            print("Thank you for using the calculator!")
            break

        else:
            print("Invalid choice")
            continue

        again = input("Do you want another calculation? (y/n): ").lower()
        if again != "y":
            print("Thank you for using the calculator!")
            break


if __name__ == "__main__":
    main()