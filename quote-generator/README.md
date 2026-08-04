# 💬 Random Quote / Affirmation Generator

A command-line tool that pulls a random quote or affirmation from a local JSON file, filterable by category, with the ability to add new quotes that persist across runs.

## Features

- **Random quote** — instantly displays a random quote from the full collection.
- **Filter by category** — lists all available categories dynamically (derived from the data, not hardcoded) and pulls a random quote from the chosen one.
- **Add new quotes** — appends a new quote to `quotes.json`, with sensible defaults (`Unknown` author, `general` category) when left blank.
- Handles a missing or corrupted `quotes.json` gracefully instead of crashing.
- Core logic (loading, filtering, adding) is fully separated from user input/output, so it's independently unit-tested.

## Demo

```
========== RANDOM QUOTE GENERATOR ==========
 1. Get a Random Quote
 2. Get a Random Quote by Category
 3. Add a New Quote
 4. Exit
=============================================
Enter your choice: 1

"The only way to do great work is to love what you do."

— Steve Jobs
```

## Project Structure

```
quote-generator/
├── project.py           # main program (menu loop + core logic)
├── test_project.py      # pytest test suite
├── quotes.json          # seed data (20 quotes across 3 categories)
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/contactsivaranjaniwork-netizen/Python-Projects.git
cd python-portfolio/quote-generator
pip install -r requirements.txt
```

## Usage

```bash
python3 project.py
```

Choose an option from the menu — get a random quote, filter by category, add a new one, or exit.

## Running Tests

```bash
pytest test_project.py -v
```

The test suite covers:
- Correct category extraction from mixed/missing data
- Random selection from the full list and from a filtered category
- `None` returned (not a crash) when no quotes match
- Adding a quote returns a new list without mutating the original
- Blank author/category default correctly to `Unknown`/`general`
- Empty quote text raises `ValueError`
- Quote formatting output, including missing-author fallback

## Design Notes

The program separates **pure logic** from **I/O**:

| Function | Responsibility |
|---|---|
| `load_quotes(filepath)` | Reads JSON from disk; handles missing/corrupted files |
| `save_quotes(quotes, filepath)` | Writes the quote list back to disk |
| `get_categories(quotes)` | Pure — returns sorted unique categories |
| `get_random_quote(quotes, category=None)` | Pure — random selection, optionally filtered |
| `add_quote(quotes, text, author, category)` | Pure — returns a new list with validation, no mutation |
| `format_quote(quote)` | Pure — formats a quote dict for display |
| `main()` | Top-level menu loop, all `input()`/`print()` |

This separation is what makes `get_categories`, `get_random_quote`, `add_quote`, and `format_quote` directly testable with `pytest`, without needing to mock `input()`.

## Possible Improvements

- "Quote of the Day" mode — deterministically pick the same quote each day using a date-based random seed
- Fetch quotes from a public API (e.g., ZenQuotes) as a fallback when the local list runs low
- Export favorite quotes to a text file or shareable image
- Add a `--daily` CLI flag to print one quote and exit (useful for cron jobs or terminal startup)

## License

Part of the [Python Project Portfolio](../README.md) — see the root [LICENSE](../LICENSE) file.
