"""
QR Code Generator (CLI)
Converts user-entered text or a URL into a downloadable QR code image.

Structure:
- generate_qr_code / build_filename: image + path generation, testable
- log_generation / read_history / format_history: history I/O and formatting
- main: top-level menu loop
"""

import os
import json
from pathlib import Path
from datetime import datetime

import qrcode

HISTORY_FILE = "qr_history.json"
OUTPUT_DIR = Path("qr_codes")


def generate_qr_code(text, filepath, fill_color="black", back_color="white"):
    """
    Generate a QR code image encoding `text` and save it to `filepath`.
    Creates the parent directory if it doesn't exist.
    Returns the filepath (as a string) on success.
    Raises ValueError if text is empty/whitespace-only.
    """
    if not text or not text.strip():
        raise ValueError("Text to encode cannot be empty")

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(filepath)

    return str(filepath)


def build_filename(output_dir=OUTPUT_DIR):
    """
    Build a unique, timestamp-based filename inside output_dir.
    Ensures output_dir exists. Returns a Path object.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return output_dir / f"qr_{timestamp}.png"


def log_generation(text, filepath, history_file=HISTORY_FILE):
    """Append a new QR generation record to the JSON history file."""
    new_entry = {
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "original_text": text,
        "filename": str(filepath),
    }

    history = read_history(history_file) or []
    history.append(new_entry)

    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def read_history(history_file=HISTORY_FILE):
    """
    Return the list of past generation records from the history file.
    Returns an empty list if the file doesn't exist, is corrupted, or is empty.
    """
    if not os.path.exists(history_file):
        return []

    try:
        with open(history_file, "r", encoding="utf-8") as file:
            history = json.load(file)
    except json.JSONDecodeError:
        return []

    if not isinstance(history, list):
        return []

    return history


def format_history(history):
    """Return a formatted multi-line string summarizing generation history."""
    if not history:
        return "No QR codes generated yet."

    lines = [f"{'Timestamp':<20} | {'Output Filename':<30} | Original Text", "-" * 80]
    for entry in history:
        lines.append(
            f"{entry['timestamp']:<20} | {entry['filename']:<30} | {entry['original_text']}"
        )
    return "\n".join(lines)


def main():
    while True:
        print(
            "\n===== QR CODE GENERATOR =====\n"
            "1. Generate a QR Code\n"
            "2. View Generation History\n"
            "3. Exit\n"
            "=============================="
        )
        choice = input("Choose an option: ")

        if choice == "1":
            user_input = input("Enter text or URL to encode: ")
            try:
                filepath = build_filename(OUTPUT_DIR)
                generate_qr_code(user_input, filepath)
                print(f"QR code saved to: {filepath}")
                log_generation(user_input, filepath)
            except ValueError as e:
                print(f"Error: {e}")
            except OSError as e:
                print(f"Could not save QR code: {e}")

        elif choice == "2":
            history = read_history()
            print(f"\n{format_history(history)}")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()