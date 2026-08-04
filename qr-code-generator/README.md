# 🔳 QR Code Generator

A command-line tool that converts any text or URL into a QR code image, saved to disk with an automatically generated filename and a searchable generation history.

## Features

- **Generate QR codes** — encode any text (URLs, plain text, contact info, Wi-Fi credentials) into a PNG image.
- **Automatic file naming** — each QR code is saved with a unique, timestamp-based filename inside a `qr_codes/` folder, created automatically if it doesn't exist.
- **Generation history** — every generated code is logged to `qr_history.json` with the original text, output filename, and timestamp; viewable anytime from the menu.
- Empty/whitespace-only input is rejected with a clear message instead of generating a blank code.
- File-write errors are caught and reported cleanly instead of crashing the program.
- Core image-generation and logging logic is fully separated from user input/output, so it's independently unit-tested.

## Demo

```
===== QR CODE GENERATOR =====
1. Generate a QR Code
2. View Generation History
3. Exit
==============================
Choose an option: 1
Enter text or URL to encode: https://github.com/yourusername
QR code saved to: qr_codes/qr_20260729_143022_512034.png

Choose an option: 2

Timestamp            | Output Filename                | Original Text
--------------------------------------------------------------------------------
29-07-2026 14:30:22  | qr_codes/qr_20260729_143022_512034.png | https://github.com/yourusername
```

## Project Structure

```
qr-code-generator/
├── project.py         # main program (menu loop + QR/history logic)
├── test_project.py     # pytest test suite
├── qr_codes/            # generated QR images (created automatically)
├── qr_history.json      # generation log (created automatically)
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/contactsivaranjaniwork-netizen/Python-Projects.git
cd python-portfolio/qr-code-generator
pip install -r requirements.txt
```

## Usage

```bash
python3 project.py
```

Choose to generate a new QR code or view the history of everything you've generated so far.

## Running Tests

```bash
pytest test_project.py -v
```

The test suite covers:
- A QR code image is actually created at the expected path
- Empty/whitespace-only text raises `ValueError`
- Missing output directories are created automatically
- Filenames generated in quick succession are unique
- History logging and reading round-trip correctly (using `pytest`'s `tmp_path`, so tests never touch your real history file)
- Corrupted history files are handled gracefully, returning an empty list instead of crashing
- History formatting produces the expected display text, including the empty-history case

## Design Notes

The program separates **pure logic** from **I/O**:

| Function | Responsibility |
|---|---|
| `generate_qr_code(text, filepath, fill_color, back_color)` | Creates and saves the QR image; validates text, creates missing directories |
| `build_filename(output_dir)` | Generates a unique, timestamp-based filename; ensures the directory exists |
| `log_generation(text, filepath, history_file)` | Appends a record to the JSON history file |
| `read_history(history_file)` | Reads and returns past generation records (handles missing/corrupted files) |
| `format_history(history)` | Formats history records into display text |
| `main()` | Top-level menu loop |

This separation is what makes every function directly testable with `pytest` against temporary files, without needing to touch your real `qr_codes/` folder or `qr_history.json`.

### A note on JSON serialization

Every value stored in the history log is explicitly converted with `str()` before being written, and `json.dump(..., default=str)` is used as a safety net — this prevents crashes like `TypeError: Object of type WindowsPath is not JSON serializable`, which happens if a `pathlib.Path` object (rather than a string) is accidentally passed into `json.dump()`.

## Possible Improvements

- Support batch generation from a CSV/text file of multiple lines to encode
- Add a `--decode` mode to read an existing QR image and print its contents (`pyzbar`)
- Embed a logo/image in the center of the generated QR code
- Add a small Tkinter GUI wrapper around the same core functions
- Auto-detect URL-like input and prepend `https://` if missing

## License

Part of the [Python Project Portfolio](../README.md) — see the root [LICENSE](../LICENSE) file.
