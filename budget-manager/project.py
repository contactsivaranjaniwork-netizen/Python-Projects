"""
Personal Budget Manager (CLI)
Tracks income/expense transactions, custom categories, and per-category
budget limits, with monthly summaries that reflect budget usage.

Structure:
- load_transactions / save_transactions: the ONLY functions touching the ledger file
- add_transaction / edit_transaction / filter_transactions: pure, testable
- get_monthly_summary / get_balance / is_over_budget / get_budget_alert_message: pure, testable
- format_table / format_transactions_table / format_monthly_summary / format_balance: pure formatting
- load_categories / save_categories / load_category_budgets / save_category_budget: settings I/O
- main: top-level menu loop
"""

import csv
import os
from datetime import datetime

BUDGET_FILE = "budget.csv"
CATEGORY_FILE = "categories.txt"
BUDGET_LIMITS_FILE = "category_budgets.txt"

FIELDNAMES = ["transaction_id", "date", "type", "amount", "category", "description"]

DEFAULT_INCOME_CATS = ["Salary", "Freelance", "Gifts", "Other"]
DEFAULT_EXPENSE_CATS = ["Food", "Rent", "Utilities", "Transport", "Other"]


# --------------------------------------------------------------------------
# Transaction persistence (the ONLY functions that touch budget.csv)
# --------------------------------------------------------------------------

def load_transactions(filename=BUDGET_FILE):
    """
    Load transactions from a CSV file as a list of dicts, with
    transaction_id as int and amount as float.
    Returns an empty list if the file doesn't exist. Skips any
    individual row that can't be parsed instead of failing entirely.
    """
    if not os.path.exists(filename):
        return []

    transactions = []
    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                transactions.append({
                    "transaction_id": int(row["transaction_id"]),
                    "date": row["date"],
                    "type": row["type"].lower(),
                    "amount": float(row["amount"]),
                    "category": row["category"],
                    "description": row.get("description", ""),
                })
            except (KeyError, ValueError, TypeError):
                continue

    return transactions


def save_transactions(transactions, filename=BUDGET_FILE):
    """Save a list of transaction dicts to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for txn in transactions:
            writer.writerow(txn)


# --------------------------------------------------------------------------
# Transaction logic (pure)
# --------------------------------------------------------------------------

def validate_txn_type(txn_type):
    """Return the normalized type ('income'/'expense') or None if invalid."""
    txn_type = txn_type.strip().lower()
    if txn_type in ("income", "expense"):
        return txn_type
    return None


def get_next_transaction_id(transactions):
    """Return the next available transaction ID (max existing + 1, or 1)."""
    return max((t["transaction_id"] for t in transactions), default=0) + 1


def add_transaction(transactions, tx_type, amount, category, description=""):
    """
    Return a NEW list with a transaction appended (does not mutate the input).
    Raises ValueError for an invalid type, non-positive amount, or empty category.
    """
    tx_type = validate_txn_type(tx_type)
    if tx_type is None:
        raise ValueError("Transaction type must be 'income' or 'expense'")

    amount = float(amount)
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    category = category.strip()
    if not category:
        raise ValueError("Category cannot be empty")

    new_txn = {
        "transaction_id": get_next_transaction_id(transactions),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": tx_type,
        "amount": amount,
        "category": category,
        "description": description.strip(),
    }

    return transactions + [new_txn]


def get_transaction_by_id(transactions, transaction_id):
    """Return the transaction dict with the matching ID, or None if not found."""
    for txn in transactions:
        if txn["transaction_id"] == transaction_id:
            return txn
    return None


def edit_transaction(transactions, transaction_id, updates, valid_categories=None):
    """
    Return a NEW list with the matching transaction's fields updated.

    If `updates` changes 'type' without also changing 'category', and
    valid_categories (a dict like {'income': [...], 'expense': [...]})
    is provided, raises ValueError if the transaction's resulting category
    isn't valid for its new type -- this prevents ending up with, e.g.,
    type='income' but category='Food'.

    Raises ValueError if transaction_id doesn't exist.
    """
    current = get_transaction_by_id(transactions, transaction_id)
    if current is None:
        raise ValueError(f"No transaction found with ID {transaction_id}")

    new_type = updates.get("type", current["type"])
    new_category = updates.get("category", current["category"])

    if valid_categories is not None and "type" in updates and "category" not in updates:
        allowed = valid_categories.get(new_type, [])
        if not any(c.lower() == new_category.lower() for c in allowed):
            raise ValueError(
                f"Category '{new_category}' is not valid for type '{new_type}'; "
                "please also provide a new category"
            )

    return [
        {**txn, **updates} if txn["transaction_id"] == transaction_id else txn
        for txn in transactions
    ]


def filter_transactions(transactions, tx_type=None, category=None, search=None):
    """
    Return the subset of transactions matching all given filters
    (case-insensitive). Any filter left as None is ignored.
    """
    result = transactions

    if tx_type is not None:
        result = [t for t in result if t["type"] == tx_type.lower()]

    if category is not None:
        result = [t for t in result if t["category"].lower() == category.lower()]

    if search is not None:
        needle = search.lower()
        result = [
            t for t in result
            if needle in t["category"].lower()
            or needle in t["description"].lower()
            or needle in t["type"].lower()
        ]

    return result


def get_balance(transactions):
    """Return (total_income, total_expense, net_balance)."""
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    return total_income, total_expense, total_income - total_expense


def is_over_budget(spent, limit):
    """Return True if a limit is set and spent exceeds it."""
    return limit is not None and spent > limit


def get_current_month():
    """Return the current month as 'YYYY-MM'."""
    return datetime.now().strftime("%Y-%m")


def get_category_spent(transactions, category, month=None):
    """
    Return total expense spending in a category, optionally restricted
    to a specific month ('YYYY-MM'). If month is None, sums all-time.
    """
    total = 0.0
    for t in transactions:
        if t["type"] != "expense" or t["category"].lower() != category.lower():
            continue
        if month is not None and not t["date"].startswith(month):
            continue
        total += t["amount"]
    return total


def get_monthly_summary(transactions, budgets=None):
    """
    Aggregate transactions into a per-month summary:
        {
          "2026-08": {
            "income": ..., "expense": ..., "net": ...,
            "categories": {
              "Food": {"spent": ..., "limit": ..., "remaining": ..., "over_budget": ...},
              ...
            }
          },
          ...
        }
    `budgets` is a dict of {category_lowercase: limit}. Categories with no
    budget set get limit/remaining = None and over_budget = False.
    """
    if budgets is None:
        budgets = {}

    raw = {}
    for txn in transactions:
        month = txn["date"].split(" ")[0][:7]
        if month not in raw:
            raw[month] = {"income": 0.0, "expense": 0.0, "categories": {}}

        raw[month][txn["type"]] += txn["amount"]

        if txn["type"] == "expense":
            cat = txn["category"]
            raw[month]["categories"][cat] = raw[month]["categories"].get(cat, 0.0) + txn["amount"]

    summary = {}
    for month, data in raw.items():
        category_breakdown = {}
        for category, spent in data["categories"].items():
            limit = budgets.get(category.lower())
            category_breakdown[category] = {
                "spent": spent,
                "limit": limit,
                "remaining": (limit - spent) if limit is not None else None,
                "over_budget": is_over_budget(spent, limit),
            }

        summary[month] = {
            "income": data["income"],
            "expense": data["expense"],
            "net": data["income"] - data["expense"],
            "categories": category_breakdown,
        }

    return summary


def get_budget_alert_message(transactions, category, budgets, month=None):
    """
    Return a warning string if `category`'s spending for the given month
    (defaults to the current month) exceeds its budget limit, else None.
    """
    if month is None:
        month = get_current_month()

    limit = budgets.get(category.lower())
    if limit is None:
        return None

    spent = get_category_spent(transactions, category, month=month)
    if is_over_budget(spent, limit):
        return (
            f"ALERT: Category '{category}' exceeded its monthly budget! "
            f"Limit: ${limit:.2f} | Spent this month: ${spent:.2f}"
        )
    return None


def get_unique_categories(transactions):
    """Return (income_categories, expense_categories) actually used in transactions."""
    income = sorted({t["category"] for t in transactions if t["type"] == "income"})
    expense = sorted({t["category"] for t in transactions if t["type"] == "expense"})
    return income, expense


# --------------------------------------------------------------------------
# Formatting (pure — returns strings, never prints)
# --------------------------------------------------------------------------

def format_table(rows, headers):
    """Return a formatted table string for the given rows/headers."""
    if not rows:
        return "Empty dataset."

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    divider = "-" * len(header_line)

    lines = [divider, header_line, divider]
    for row in rows:
        lines.append(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))
    lines.append(divider)

    return "\n".join(lines)


def format_transactions_table(transactions):
    """Format a list of transactions as a display-ready table string."""
    headers = ["ID", "Date", "Type", "Amount", "Category", "Description"]
    rows = [
        [t["transaction_id"], t["date"], t["type"], f"${t['amount']:.2f}", t["category"], t["description"]]
        for t in transactions
    ]
    return format_table(rows, headers)


def format_balance(income, expense, net):
    """Format a balance summary as a display string."""
    return (
        f"Total Income : ${income:.2f}\n"
        f"Total Expenses: ${expense:.2f}\n"
        f"Net Balance   : ${net:.2f}"
    )


def format_monthly_summary(summary):
    """
    Format a get_monthly_summary(...) result into a display string,
    including per-category budget status for each month.
    """
    if not summary:
        return "No transactions recorded yet."

    lines = []
    for month in sorted(summary.keys(), reverse=True):
        data = summary[month]
        lines.append(f"=== {month} ===")
        lines.append(f"Income: ${data['income']:.2f}  Expense: ${data['expense']:.2f}  Net: ${data['net']:.2f}")

        if data["categories"]:
            lines.append("Category breakdown:")
            for category in sorted(data["categories"]):
                info = data["categories"][category]
                if info["limit"] is not None:
                    status = "OVER BUDGET" if info["over_budget"] else "within budget"
                    lines.append(
                        f"  - {category}: spent ${info['spent']:.2f} / limit ${info['limit']:.2f} "
                        f"({status}, remaining ${info['remaining']:.2f})"
                    )
                else:
                    lines.append(f"  - {category}: spent ${info['spent']:.2f} (no budget set)")
        lines.append("")

    return "\n".join(lines).rstrip()


# --------------------------------------------------------------------------
# Categories & budget limits persistence
# --------------------------------------------------------------------------

def load_categories(filename=CATEGORY_FILE):
    """
    Load income/expense category lists from a text file with
    [INCOME]/[EXPENSE] section markers. Creates the file with defaults
    if it doesn't exist. Falls back to defaults (without overwriting
    the file) if it exists but is malformed or empty.
    """
    if not os.path.exists(filename):
        save_categories(DEFAULT_INCOME_CATS, DEFAULT_EXPENSE_CATS, filename)
        return list(DEFAULT_INCOME_CATS), list(DEFAULT_EXPENSE_CATS)

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
    except OSError:
        return list(DEFAULT_INCOME_CATS), list(DEFAULT_EXPENSE_CATS)

    current_type = None
    income_list, expense_list = [], []

    for line in lines:
        line = line.strip()
        if line == "[INCOME]":
            current_type = "income"
        elif line == "[EXPENSE]":
            current_type = "expense"
        elif line and not line.startswith("#"):
            if current_type == "income":
                income_list.append(line)
            elif current_type == "expense":
                expense_list.append(line)

    if not income_list and not expense_list:
        # File exists but had no recognizable section markers/content at
        # all -- fall back to defaults rather than leaving the user with
        # empty category lists (which would make adding transactions
        # impossible).
        return list(DEFAULT_INCOME_CATS), list(DEFAULT_EXPENSE_CATS)

    return income_list, expense_list


def save_categories(income_list, expense_list, filename=CATEGORY_FILE):
    """Save income/expense category lists to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("[INCOME]\n")
        for cat in sorted(income_list):
            file.write(f"{cat}\n")
        file.write("\n[EXPENSE]\n")
        for cat in sorted(expense_list):
            file.write(f"{cat}\n")


def load_category_budgets(filename=BUDGET_LIMITS_FILE):
    """
    Load {category_lowercase: limit} from a text file of 'category:amount'
    lines. Skips individual malformed lines instead of aborting the
    entire parse on the first bad one. Returns {} if the file is missing.
    """
    limits = {}
    if not os.path.exists(filename):
        return limits

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            if ":" not in line:
                continue
            category, _, amount_str = line.strip().partition(":")
            try:
                limits[category.lower()] = float(amount_str)
            except ValueError:
                continue  # skip just this line, keep parsing the rest

    return limits


def save_category_budget(category, amount, filename=BUDGET_LIMITS_FILE):
    """Set (or update) a single category's budget limit and save all limits."""
    amount = float(amount)
    if amount < 0:
        raise ValueError("Budget limit cannot be negative")

    limits = load_category_budgets(filename)
    limits[category.lower()] = amount

    with open(filename, "w", encoding="utf-8") as file:
        for cat, amt in limits.items():
            file.write(f"{cat}:{amt}\n")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def prompt_category(prompt_label, options):
    """Prompt until the user enters a category matching one of `options` (case-insensitive)."""
    options_str = ", ".join(options)
    while True:
        print(f"\nAvailable {prompt_label} categories: {options_str}")
        user_cat = input("Enter the category: ").strip()
        matched = next((c for c in options if c.lower() == user_cat.lower()), None)
        if matched:
            return matched
        print("Invalid category! You must select an entry from the options above.")


def main():
    transactions = load_transactions()

    while True:
        active_income_cats, active_expense_cats = load_categories()
        budgets = load_category_budgets()

        print("\n=====  PERSONAL BUDGET MANAGER  =====")
        print("1. Add Transaction")
        print("2. Add Transaction Category")
        print("3. View All Transactions")
        print("4. View All Income")
        print("5. View All Expenses")
        print("6. View Monthly Summary")
        print("7. View Current Balance")
        print("8. Set Budget on Category")
        print("9. Search Transaction")
        print("10. Edit Transaction")
        print("11. Exit")
        print("========================================")

        choice = input("Enter your choice (1-11): ").strip()
        if choice not in [str(i) for i in range(1, 12)]:
            print("Invalid choice. Please choose exactly between 1 and 11.")
            continue

        if choice == "1":
            print("\n--- Add Transaction ---")
            while True:
                tx_type = input("Do you want to add expense / income? ").strip().lower()
                if validate_txn_type(tx_type):
                    break
                print("Invalid input! Please type exactly 'income' or 'expense'.\n")

            while True:
                try:
                    amount = float(input("Enter the amount: "))
                    if amount <= 0:
                        print("Amount must be greater than zero.\n")
                        continue
                    break
                except ValueError:
                    print("Invalid amount! Please enter a valid decimal number.\n")

            csv_inc, csv_exp = get_unique_categories(transactions)
            income_options = sorted(set(active_income_cats + csv_inc))
            expense_options = sorted(set(active_expense_cats + csv_exp))
            allowed_options = income_options if tx_type == "income" else expense_options
            category = prompt_category(tx_type.upper(), allowed_options)

            description = input("Enter the description: ").strip()

            transactions = add_transaction(transactions, tx_type, amount, category, description)
            save_transactions(transactions)
            new_txn = transactions[-1]
            print(f"Successfully added {tx_type} of ${new_txn['amount']:.2f} (ID: {new_txn['transaction_id']})")

            if tx_type == "expense":
                alert = get_budget_alert_message(transactions, category, budgets)
                if alert:
                    print(alert)

        elif choice == "2":
            print("\n--- Add Transaction Category ---")
            while True:
                cat_type = input("Add category for expense or income? ").strip().lower()
                if validate_txn_type(cat_type):
                    break
                print("Invalid input! Choose exactly 'income' or 'expense'.\n")

            csv_inc, csv_exp = get_unique_categories(transactions)
            current_options = (
                sorted(set(active_income_cats + csv_inc)) if cat_type == "income"
                else sorted(set(active_expense_cats + csv_exp))
            )

            print(f"\nExisting {cat_type.upper()} categories: {', '.join(current_options)}")
            new_cat = input("Enter new custom category name to add: ").strip()

            if not new_cat:
                print("Category name cannot be empty.")
            elif any(c.lower() == new_cat.lower() for c in current_options):
                print(f"'{new_cat}' already exists!")
            else:
                if cat_type == "income":
                    active_income_cats.append(new_cat)
                else:
                    active_expense_cats.append(new_cat)
                save_categories(active_income_cats, active_expense_cats)
                print(f"Added and saved '{new_cat}' permanently!")

        elif choice == "3":
            print("\n--- View All Transactions ---")
            print(format_transactions_table(transactions))

        elif choice == "4":
            print("\n--- View All Income ---")
            print(format_transactions_table(filter_transactions(transactions, tx_type="income")))

        elif choice == "5":
            print("\n--- View All Expenses ---")
            print(format_transactions_table(filter_transactions(transactions, tx_type="expense")))

        elif choice == "6":
            print("\n--- View Monthly Summary ---")
            summary = get_monthly_summary(transactions, budgets)
            print(format_monthly_summary(summary))

        elif choice == "7":
            print("\n--- View Current Balance ---")
            income, expense, net = get_balance(transactions)
            print(format_balance(income, expense, net))

        elif choice == "8":
            print("\n--- Set Budget Limit on Category ---")
            csv_inc, csv_exp = get_unique_categories(transactions)
            all_expense_options = sorted(set(active_expense_cats + csv_exp))
            print(f"Available Expense Categories: {', '.join(all_expense_options)}")
            tgt_cat = input("Select expense category to set a budget limit on: ").strip()
            matched_cat = next((c for c in all_expense_options if c.lower() == tgt_cat.lower()), None)

            if matched_cat:
                while True:
                    try:
                        limit_amt = float(input(f"Enter budget limit for '{matched_cat}': $"))
                        save_category_budget(matched_cat, limit_amt)
                        print(f"Limit set! Category '{matched_cat}' capped at ${limit_amt:.2f} per month")
                        break
                    except ValueError as e:
                        print(f"Invalid input: {e}")
            else:
                print("Category not found.")

        elif choice == "9":
            print("\n--- Search Transaction ---")
            query = input("Enter search term (Category, Description, or Type): ").strip()
            print(format_transactions_table(filter_transactions(transactions, search=query)))

        elif choice == "10":
            print("\n--- Edit Transaction Record ---")
            try:
                target_id = int(input("Enter Transaction ID to edit: ").strip())
            except ValueError:
                print("Invalid ID. Please enter a number.")
                continue

            target = get_transaction_by_id(transactions, target_id)
            if target is None:
                print("Transaction ID not found.")
                continue

            print(
                f"\nTarget Found: Type={target['type']} | Amt={target['amount']} | "
                f"Category={target['category']} | Desc={target['description']}"
            )

            updates = {}

            new_type = input("New type ('income'/'expense') or Enter to keep current: ").strip().lower()
            if new_type and validate_txn_type(new_type):
                updates["type"] = validate_txn_type(new_type)

            new_amt = input("New amount or Enter to keep current: ").strip()
            if new_amt:
                try:
                    parsed_amt = float(new_amt)
                    if parsed_amt > 0:
                        updates["amount"] = parsed_amt
                    else:
                        print("Amount must be positive. Keeping original value.")
                except ValueError:
                    print("Invalid amount entered. Keeping original value.")

            effective_type = updates.get("type", target["type"])
            csv_inc, csv_exp = get_unique_categories(transactions)
            opts = (
                sorted(set(active_income_cats + csv_inc)) if effective_type == "income"
                else sorted(set(active_expense_cats + csv_exp))
            )
            print(f"Choices: {', '.join(opts)}")
            new_cat = input("New category or Enter to skip: ").strip()
            if new_cat:
                matched_cat = next((c for c in opts if c.lower() == new_cat.lower()), None)
                if matched_cat:
                    updates["category"] = matched_cat
                else:
                    print("Category not recognized. Keeping original value.")

            new_desc = input("New description or Enter to skip: ").strip()
            if new_desc:
                updates["description"] = new_desc

            try:
                valid_categories = {"income": active_income_cats, "expense": active_expense_cats}
                transactions = edit_transaction(transactions, target_id, updates, valid_categories)
                save_transactions(transactions)
                print("Transaction updated successfully!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "11":
            print("\nExiting Personal Budget Manager. Goodbye!")
            break


if __name__ == "__main__":
    main()