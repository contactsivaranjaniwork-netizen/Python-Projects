"""
Countdown Timer / Pomodoro Clock (CLI)
Runs work/break intervals and plays a sound alert when each interval ends.
 
Structure:
- format_time / build_pomodoro_sequence: pure, testable (no time.sleep)
- run_countdown / run_sequence / play_alert: actual timing + I/O
- log_session / read_history / get_session_summary: history I/O + pure aggregation
- load_settings / save_settings: settings persistence
- main: top-level menu loop
"""
 
import os
import sys
import csv
import json
import time
from datetime import datetime
 
LOG_FILE = "pomodoro_history.csv"
SETTINGS_FILE = "pomodoro_settings.json"
 
DEFAULT_SETTINGS = {
    "work_min": 25,
    "short_break_min": 5,
    "long_break_min": 15,
    "cycles_before_long_break": 4,
}
 
 
def format_time(seconds):
    """Format a whole number of seconds as MM:SS."""
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"
 
 
def build_pomodoro_sequence(work_min, short_break_min, long_break_min,
                             cycles_before_long_break, total_cycles):
    """
    Build the ordered list of intervals for a Pomodoro run, WITHOUT
    running them (no time.sleep here — this is what makes it testable
    instantly instead of waiting through real minutes).
 
    Returns a list of (label, log_type, duration_min) tuples. Every work
    session is followed by a break: a long break every
    `cycles_before_long_break` work sessions, a short break otherwise.
 
    Raises ValueError if any duration is not positive, or if
    cycles_before_long_break/total_cycles is not a positive integer.
    """
    if work_min <= 0 or short_break_min <= 0 or long_break_min <= 0:
        raise ValueError("All durations must be positive")
    if cycles_before_long_break <= 0:
        raise ValueError("cycles_before_long_break must be a positive integer")
    if total_cycles <= 0:
        raise ValueError("total_cycles must be a positive integer")
 
    sequence = []
    for i in range(1, total_cycles + 1):
        sequence.append((f"Work Session {i}", "Work", work_min))
        if i % cycles_before_long_break == 0:
            sequence.append(("Long Break", "Long Break", long_break_min))
        else:
            sequence.append(("Short Break", "Short Break", short_break_min))
 
    return sequence
 
 
def play_alert():
    """Play a terminal bell sound."""
    sys.stdout.write("\a")
    sys.stdout.flush()
 
 
def run_countdown(duration_min, label):
    """
    Run a live countdown for duration_min minutes, updating the display
    each second. Plays a bell and returns True on natural completion;
    returns False if interrupted early via Ctrl+C.
    """
    total_seconds = int(duration_min * 60)
    print(f"\n--- Starting {label} ({duration_min} min) ---")
    print("Press Ctrl+C to stop this session early.")
 
    try:
        while total_seconds > 0:
            sys.stdout.write(f"\r{label} — Time remaining: {format_time(total_seconds)}")
            sys.stdout.flush()
            time.sleep(1)
            total_seconds -= 1
        sys.stdout.write(f"\r{label} — Time remaining: 00:00\n")
    except KeyboardInterrupt:
        print("\nSession interrupted by user.")
        return False
 
    play_alert()
    print(f"{label} complete!")
    return True
 
 
def run_sequence(sequence, log_file=LOG_FILE):
    """
    Run each (label, log_type, duration_min) interval in sequence,
    logging each one that completes successfully. Stops early (without
    exiting the whole program) if the user interrupts a countdown.
 
    Returns True if the full sequence completed, False if interrupted early.
    """
    for label, log_type, duration_min in sequence:
        completed = run_countdown(duration_min, label)
        if not completed:
            return False
        log_session(log_type, duration_min, log_file=log_file)
    return True
 
 
def init_log_file(log_file=LOG_FILE):
    """Create the CSV log file with headers if it doesn't exist."""
    if not os.path.exists(log_file):
        with open(log_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Type", "Duration_Mins"])
 
 
def log_session(session_type, duration_min, log_file=LOG_FILE):
    """Append a completed session to the CSV log file."""
    init_log_file(log_file)
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open(log_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, session_type, duration_min])
 
 
def read_history(log_file=LOG_FILE):
    """
    Return the list of logged sessions as dicts.
    Returns an empty list if the log file doesn't exist.
    """
    if not os.path.exists(log_file):
        return []
 
    with open(log_file, mode="r", encoding="utf-8") as file:
        return list(csv.DictReader(file))
 
 
def get_session_summary(history, date_str=None, session_type="Work"):
    """
    Aggregate a history list into (count, total_minutes) for a given
    date (defaults to today, format DD-MM-YYYY) and session type.
    """
    if date_str is None:
        date_str = datetime.now().strftime("%d-%m-%Y")
 
    count = 0
    total_minutes = 0
    for row in history:
        log_date = row["Timestamp"].split(" ")[0]
        if log_date == date_str and row["Type"] == session_type:
            count += 1
            total_minutes += int(row["Duration_Mins"])
 
    return count, total_minutes
 
 
def format_summary(count, total_minutes):
    """Format a session summary as a display string."""
    if count == 0:
        return "No work sessions recorded for today yet."
    return f"Today: {count} work session(s) completed, {total_minutes} minutes focused."
 
 
def load_settings(config_file=SETTINGS_FILE):
    """
    Load Pomodoro settings from a JSON file, falling back to defaults
    if the file doesn't exist or is corrupted.
    """
    if not os.path.exists(config_file):
        return dict(DEFAULT_SETTINGS)
 
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            settings = json.load(file)
    except json.JSONDecodeError:
        return dict(DEFAULT_SETTINGS)
 
    merged = dict(DEFAULT_SETTINGS)
    if isinstance(settings, dict):
        merged.update(settings)
    return merged
 
 
def save_settings(settings, config_file=SETTINGS_FILE):
    """Save Pomodoro settings to a JSON file."""
    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)
 
 
def get_positive_int(prompt, minimum=1, maximum=180):
    """Repeatedly prompt until the user enters an int within [minimum, maximum]."""
    while True:
        try:
            value = int(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Please enter a value between {minimum} and {maximum}.")
        except ValueError:
            print("Invalid input. Enter a whole number.")
 
 
def main():
    settings = load_settings()
 
    while True:
        print(
            "\n===== POMODORO CLOCK =====\n"
            "1. Start a Pomodoro Session\n"
            "2. Custom Timer\n"
            "3. View Session History\n"
            "4. Settings\n"
            "5. Exit\n"
            "=============================="
        )
        choice = input("Choose an option: ")
 
        if choice == "1":
            total_cycles = get_positive_int(
                "How many work sessions do you want to complete? ", minimum=1, maximum=20
            )
            sequence = build_pomodoro_sequence(
                settings["work_min"],
                settings["short_break_min"],
                settings["long_break_min"],
                settings["cycles_before_long_break"],
                total_cycles,
            )
            completed = run_sequence(sequence)
            if not completed:
                print("Pomodoro session ended early. Back to the main menu.")
 
        elif choice == "2":
            print("=== Custom Timer ===")
            work = get_positive_int("How long do you want to work (minutes)? ")
            brk = get_positive_int("How long is your break (minutes)? ")
            sequence = [
                ("Custom Work", "Work", work),
                ("Custom Break", "Custom Break", brk),
            ]
            completed = run_sequence(sequence)
            if not completed:
                print("Custom timer ended early. Back to the main menu.")
 
        elif choice == "3":
            history = read_history()
            count, total_minutes = get_session_summary(history)
            print(f"\n{format_summary(count, total_minutes)}")
 
        elif choice == "4":
            print("\n--- Settings ---")
            print(f"1. Work duration: {settings['work_min']} min")
            print(f"2. Short break duration: {settings['short_break_min']} min")
            print(f"3. Long break duration: {settings['long_break_min']} min")
            print(f"4. Work sessions before a long break: {settings['cycles_before_long_break']}")
            print("5. Back to main menu")
            setting_choice = input("Choose a setting to change: ")
 
            if setting_choice == "1":
                settings["work_min"] = get_positive_int("New work duration (minutes): ")
                save_settings(settings)
            elif setting_choice == "2":
                settings["short_break_min"] = get_positive_int("New short break duration (minutes): ")
                save_settings(settings)
            elif setting_choice == "3":
                settings["long_break_min"] = get_positive_int("New long break duration (minutes): ")
                save_settings(settings)
            elif setting_choice == "4":
                settings["cycles_before_long_break"] = get_positive_int(
                    "New number of work sessions before a long break: ", minimum=1, maximum=20
                )
                save_settings(settings)
            elif setting_choice == "5":
                pass
            else:
                print("Invalid choice.")
 
        elif choice == "5":
            print("Goodbye!")
            break
 
        else:
            print("Enter a valid input")
 
 
if __name__ == "__main__":
    main()
 
