# 🔐 Random Password Generator

A command-line tool that generates cryptographically strong, random passwords based on user-defined length and character-set rules, checks the strength of existing passwords, and keeps a metadata-only generation history.

## Features

- **Custom password generation** — choose length (4–128 characters) and which character sets to include: uppercase, lowercase, digits, symbols.
- **Guaranteed character coverage** — every selected character set is guaranteed to appear at least once in the generated password, by construction (not by chance).
- **Cryptographically secure randomness** — uses Python's `secrets` module throughout, not `random`, since password generation is security-sensitive.
- **Password strength checker** — rates any password as Weak / Moderate / Strong based on length and character-set diversity.
- **Privacy-conscious history** — logs the *metadata* of each generation (timestamp, length, which character sets were used) to `log.json`, but **never the password itself**.
- Invalid input (bad length, no character set selected, empty password check) is caught and reported clearly instead of crashing or hanging.

## Demo

```
===== PASSWORD GENERATOR =====
1. Generate a Password
2. Check Password Strength
3. View Generation History
4. Exit
==============================
Choose an option: 1
Enter desired length (4-128): 16
Include uppercase letters? (y/n): y
Include lowercase letters? (y/n): y
Include digits? (y/n): y
Include symbols? (y/n): y

Generated password: 5p]m..dT-'UdRHuJ
```

```
Choose an option: 2
Enter a password to check: hunter2
Password strength: Weak
```

## Project Structure

```
password-generator/
├── project.py        # main program (menu loop + password/strength logic)
├── test_project.py    # pytest test suite
├── log.json            # generation history (created automatically; metadata only)
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/contactsivaranjaniwork-netizen/Python-Projects.git
cd python-portfolio/password-generator
pip install -r requirements.txt
```

## Usage

```bash
python3 project.py
```

Choose to generate a password, check an existing one's strength, or view past generation activity.

## Running Tests

```bash
pytest test_project.py -v
```

The test suite covers:
- Character pool construction for every combination of selected sets
- Generated passwords have the correct length
- Generated passwords only contain characters from the selected sets
- Generated passwords contain at least one character from **every** selected set, checked across many runs (guaranteed by construction, not left to chance)
- Invalid length (too short/too long), no character set selected, and length too short to fit one of each required set all raise `ValueError`
- Strength ratings for known weak/moderate/strong examples
- History logging, reading, and formatting round-trip correctly (using `pytest`'s `tmp_path`, so tests never touch your real `log.json`)

## Design Notes

The program separates **pure logic** from **I/O**:

| Function | Responsibility |
|---|---|
| `build_character_pool(...)` | Pure — combines selected character sets, validates at least one is chosen |
| `generate_password(...)` | Pure — guaranteed-correct password construction, no retry loop |
| `check_password_strength(password)` | Pure — rates strength, validates non-empty input |
| `log_generation(...)` | I/O — appends metadata-only record to the JSON log |
| `read_log(log_file)` | I/O — reads back past generation metadata |
| `format_log(log)` | Pure — formats log records into display text |
| `get_length(prompt)` / `get_yes_no(prompt)` | Input validation helpers |
| `main()` | Top-level menu loop |

### Why `secrets` instead of `random`

Python's `random` module is a pseudo-random generator designed for simulations and games — it's predictable enough that an attacker who observes enough output can potentially reconstruct its internal state and predict future values. `secrets` is built specifically for security-sensitive work like passwords, tokens, and keys, drawing from the operating system's cryptographically secure randomness source.

### Why no retry loop

An earlier design generated a random password and retried if it happened not to contain every required character set. This works most of the time, but for short lengths with many required sets, it can spin for a long time — or in some cases (e.g., asking for a 2-character password containing an uppercase letter, a digit, and a symbol), it can **never succeed and loop forever**. Instead, this version seeds one guaranteed character from each selected set up front, fills the rest randomly, and shuffles — this always terminates and is validated up front with a clear error if the requested length is too short for the selected sets.

## Possible Improvements

- Add a `--copy` flag to copy the password directly to the clipboard (`pyperclip`) instead of printing it
- Support excluding ambiguous characters (`0`/`O`, `1`/`l`) for manual typing
- Batch-generate multiple passwords at once
- Display estimated entropy (bits) alongside the strength rating
- Add a passphrase mode (e.g., `correct-horse-battery-staple`)

## License

Part of the [Python Project Portfolio](../README.md) — see the root [LICENSE](../LICENSE) file.
