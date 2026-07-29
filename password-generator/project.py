"""
Random Password Generator (CLI)
Generates passwords with user-defined length and character-set rules
(upper/lower/digits/symbols), checks password strength, and logs
generation metadata (never the password itself) to a JSON history file.

Structure:
- build_character_pool / generate_password / check_password_strength: pure, testable
- log_generation / read_log / format_log: history I/O and formatting
- main: top-level menu loop
"""

import string
import secrets
import json
import os
from datetime import datetime

LOG_FILE = "log.json"
MIN_LENGTH = 4
MAX_LENGTH = 128

CHARSETS = {
    "upper": string.ascii_uppercase,
    "lower": string.ascii_lowercase,
    "digits": string.digits,
    "symbols": string.punctuation,
}


def build_character_pool(use_upper, use_lower, use_digits, use_symbols):
    """
    Return the combined pool of allowed characters based on which
    character sets are selected (each a bool).
    Raises ValueError if no character set is selected.
    """
    pool = ""
    if use_upper:
        pool += CHARSETS["upper"]
    if use_lower:
        pool += CHARSETS["lower"]
    if use_digits:
        pool += CHARSETS["digits"]
    if use_symbols:
        pool += CHARSETS["symbols"]

    if not pool:
        raise ValueError("At least one character set must be selected")

    return pool


def _secure_shuffle(chars):
    """In-place Fisher-Yates shuffle using a cryptographically secure source."""
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]


def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """
    Generate a random password of the given length using only the
    selected character sets (each a bool). Guarantees at least one
    character from each selected set appears in the result.

    Uses `secrets` (not `random`) since this is security-sensitive.
    Construction is guaranteed-correct (no retry loop): one required
    character is seeded from each selected set, the rest is filled
    randomly from the full pool, then the whole password is shuffled.

    Raises ValueError if length is out of range, no character set is
    selected, or length is too short to include one of every
    selected set.
    """
    if length < MIN_LENGTH or length > MAX_LENGTH:
        raise ValueError(f"Length must be between {MIN_LENGTH} and {MAX_LENGTH}")

    # Reuse build_character_pool for the combined pool + "at least one
    # selected" validation, instead of duplicating that logic here.
    pool = build_character_pool(use_upper, use_lower, use_digits, use_symbols)

    # Individual sets are still needed (not just the combined pool) so we
    # can seed exactly one guaranteed character from each of them below.
    selected_sets = [
        charset
        for charset, is_selected in (
            (CHARSETS["upper"], use_upper),
            (CHARSETS["lower"], use_lower),
            (CHARSETS["digits"], use_digits),
            (CHARSETS["symbols"], use_symbols),
        )
        if is_selected
    ]

    if length < len(selected_sets):
        raise ValueError(
            f"Length must be at least {len(selected_sets)} to include "
            "one character from each selected set"
        )

    # Guarantee one character from each selected set...
    password_chars = [secrets.choice(charset) for charset in selected_sets]
    # ...then fill the remainder randomly from the full pool.
    password_chars += [secrets.choice(pool) for _ in range(length - len(selected_sets))]

    _secure_shuffle(password_chars)
    return "".join(password_chars)


def check_password_strength(password):
    """
    Rate a password's strength as 'Weak', 'Moderate', or 'Strong' based
    on length and character-set diversity.
    Raises ValueError if password is empty.
    """
    if not password:
        raise ValueError("Password cannot be empty")

    charset_count = 0
    if any(char in string.ascii_uppercase for char in password):
        charset_count += 1
    if any(char in string.ascii_lowercase for char in password):
        charset_count += 1
    if any(char in string.digits for char in password):
        charset_count += 1
    if any(char in string.punctuation for char in password):
        charset_count += 1

    length = len(password)
    if length < 8:
        return "Weak" if charset_count <= 1 else "Moderate"
    elif length <= 12:
        return "Moderate" if charset_count <= 2 else "Strong"
    else:
        return "Weak" if charset_count <= 1 else ("Moderate" if charset_count <= 2 else "Strong")


def log_generation(length, use_upper, use_lower, use_digits, use_symbols, log_file=LOG_FILE):
    """
    Append a new generation record to the JSON log file.
    Only metadata is stored (length + which character sets were used) —
    the actual password is never written to disk.
    """
    new_entry = {
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "length": length,
        "upper": use_upper,
        "lower": use_lower,
        "digits": use_digits,
        "symbols": use_symbols,
    }

    log = read_log(log_file) or []
    log.append(new_entry)

    with open(log_file, "w", encoding="utf-8") as file:
        json.dump(log, file, indent=4, default=str)


def read_log(log_file=LOG_FILE):
    """
    Return the list of past generation records from the log file.
    Returns an empty list if the file doesn't exist, is corrupted, or empty.
    """
    if not os.path.exists(log_file):
        return []

    try:
        with open(log_file, "r", encoding="utf-8") as file:
            log = json.load(file)
    except json.JSONDecodeError:
        return []

    if not isinstance(log, list):
        return []

    return log


def format_log(log):
    """Return a formatted multi-line string summarizing generation history."""
    if not log:
        return "No history found."

    lines = []
    for entry in log:
        lines.append(
            f"{entry['timestamp']} | Length: {entry['length']} | "
            f"U:{entry['upper']} L:{entry['lower']} "
            f"D:{entry['digits']} S:{entry['symbols']}"
        )
    return "\n".join(lines)


def get_length(prompt):
    """Repeatedly prompt until the user enters a length within valid bounds."""
    while True:
        try:
            value = int(input(prompt))
            if value < MIN_LENGTH or value > MAX_LENGTH:
                print(f"Please enter a length between {MIN_LENGTH} and {MAX_LENGTH}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_yes_no(prompt):
    """Repeatedly prompt until the user enters 'y' or 'n'; returns a bool."""
    while True:
        value = input(prompt).strip().lower()
        if value in ("y", "n"):
            return value == "y"
        print("Please enter 'y' or 'n'.")


def main():
    while True:
        print(
            "\n===== PASSWORD GENERATOR =====\n"
            "1. Generate a Password\n"
            "2. Check Password Strength\n"
            "3. View Generation History\n"
            "4. Exit\n"
            "=============================="
        )
        choice = input("Choose an option: ")

        if choice == "1":
            length = get_length(f"Enter desired length ({MIN_LENGTH}-{MAX_LENGTH}): ")
            use_upper = get_yes_no("Include uppercase letters? (y/n): ")
            use_lower = get_yes_no("Include lowercase letters? (y/n): ")
            use_digits = get_yes_no("Include digits? (y/n): ")
            use_symbols = get_yes_no("Include symbols? (y/n): ")

            try:
                password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
                print(f"\nGenerated password: {password}")
                log_generation(len(password), use_upper, use_lower, use_digits, use_symbols)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            check_pwd = input("Enter a password to check: ")
            try:
                strength = check_password_strength(check_pwd)
                print(f"Password strength: {strength}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            log = read_log()
            print(f"\n{format_log(log)}")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()