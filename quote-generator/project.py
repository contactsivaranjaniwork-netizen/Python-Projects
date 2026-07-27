"""
Random Quote / Affirmation Generator (CLI)
Pulls a random quote from a local JSON file and prints it on demand.

Structure:
- load_quotes / save_quotes: file I/O
- get_categories / get_random_quote / add_quote: pure, testable logic
- main: top-level menu loop
"""

import json
import random

FILENAME = "quotes.json"


def load_quotes(filepath):
    """
    Load quotes from a JSON file and return them as a list of dicts.
    Returns an empty list if the file is missing, empty, or corrupted,
    printing a friendly message in each case rather than crashing.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"'{filepath}' not found. Starting with an empty quote list.")
        return []
    except json.JSONDecodeError:
        print(f"'{filepath}' is corrupted or not valid JSON. Starting with an empty quote list.")
        return []

    if not isinstance(data, list):
        print(f"'{filepath}' does not contain a valid list of quotes. Starting with an empty quote list.")
        return []

    return data


def save_quotes(quotes, filepath):
    """Write the given list of quotes to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=4)


def get_categories(quotes):
    """Return a sorted list of unique categories present in the quotes list."""
    return sorted(set(q["category"] for q in quotes if "category" in q))


def get_random_quote(quotes, category=None):
    """
    Return a random quote dict from the list, optionally filtered by category.
    Returns None if there are no quotes (in the given category, if specified).
    """
    if category is not None:
        pool = [q for q in quotes if q.get("category") == category]
    else:
        pool = quotes

    if not pool:
        return None

    return random.choice(pool)


def add_quote(quotes, text, author, category):
    """
    Return a NEW list with a quote appended (does not mutate the input list).
    Raises ValueError if text is empty. Defaults author to 'Unknown' and
    category to 'general' when blank.
    """
    text = text.strip()
    if not text:
        raise ValueError("Quote text cannot be empty")

    author = author.strip() if author else ""
    category = category.strip().lower() if category else ""

    new_quote = {
        "text": text,
        "author": author or "Unknown",
        "category": category or "general",
    }

    return quotes + [new_quote]


def format_quote(quote):
    """Format a quote dict as a display string."""
    text = quote.get("text", "")
    author = quote.get("author", "").strip() or "Unknown"
    return f'"{text}"\n\n— {author}'


def main():
    quotes = load_quotes(FILENAME)

    while True:
        print(
            "\n========== RANDOM QUOTE GENERATOR ==========\n"
            " 1. Get a Random Quote\n"
            " 2. Get a Random Quote by Category\n"
            " 3. Add a New Quote\n"
            " 4. Exit\n"
            "============================================="
        )
        choice = input("Enter your choice: ")

        if choice == "1":
            quote = get_random_quote(quotes)
            if quote:
                print(f"\n{format_quote(quote)}\n")
            else:
                print("\nNo quotes available yet. Add one first!")

        elif choice == "2":
            categories = get_categories(quotes)
            if not categories:
                print("\nNo categories available yet.")
                continue

            print("\nAvailable Categories:")
            for index, category in enumerate(categories, 1):
                print(f"{index}. {category.capitalize()}")

            try:
                category_choice = int(input("\nSelect a category number: "))
            except ValueError:
                print("\nPlease enter a valid number.")
                continue

            if not 1 <= category_choice <= len(categories):
                print("\nInvalid selection number.")
                continue

            selected_category = categories[category_choice - 1]
            quote = get_random_quote(quotes, category=selected_category)
            if quote:
                print(f"\n{format_quote(quote)}\n")
            else:
                print("\nNo quotes found in this category.")

        elif choice == "3":
            text = input("Enter quote text: ")
            author = input("Enter author (leave blank for Unknown): ")
            category = input("Enter category (leave blank for General): ")

            try:
                quotes = add_quote(quotes, text, author, category)
                save_quotes(quotes, FILENAME)
                print("\nSuccess: Quote added and saved successfully!")
            except ValueError as e:
                print(f"\nError: {e}. Quote not saved.")

        elif choice == "4":
            print("\nExiting program. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()