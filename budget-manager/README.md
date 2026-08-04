# 💰 Personal Budget Manager

A command-line personal finance tracker: log income and expenses, organize them into custom categories, set per-category monthly budget limits, and see exactly how you're tracking against those limits right inside your monthly summary.

## Features

- **Add transactions** — income or expense, with amount, category, and description; each gets a unique auto-incrementing ID and timestamp.
- **Custom categories** — add your own income/expense categories on top of the defaults, persisted across runs.
- **View & search** — view all transactions, income only, expenses only, or search by category/description/type.
- **Edit transactions** — update type, amount, category, or description by ID, with a safeguard against ending up with a mismatched type/category (e.g., `type=income` with `category=Food`).
- **Per-category budget limits** — cap monthly spending on any expense category (e.g., "Food capped at $250/month").
- **Budget-aware Monthly Summary** — the standout feature: your monthly summary doesn't just show income/expense/net — it breaks down spending **by category with budget status inline**, flagging anything over its limit.
- **Real-time budget alerts** — get warned immediately if a new expense pushes a category over its monthly limit.
- Core logic (transaction filtering, balance calculation, monthly aggregation, budget comparison) is fully separated from user input/output, so it's independently unit-tested.

## Demo

```
===== PERSONAL BUDGET MANAGER =====
1. Add Transaction
...
8. Set Budget on Category
...
Enter your choice (1-11): 6

--- View Monthly Summary ---
=== 2026-08 ===
Income: $2000.00  Expense: $400.00  Net: $1600.00
Category breakdown:
  - Food: spent $400.00 / limit $250.00 (OVER BUDGET, remaining $-150.00)
```

That's the key feature: budget limits set in option 8 show up automatically, per month, right in the summary — no separate report needed.

## Project Structure

```
budget-manager/
├── project.py               # main program (menu loop + all logic)
├── test_project.py           # pytest test suite
├── budget.csv                  # transaction ledger (created automatically)
├── categories.txt               # income/expense categories (created automatically with defaults)
├── category_budgets.txt          # per-category budget limits (created automatically)
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/contactsivaranjaniwork-netizen/Python-Projects.git
cd Python-Projects/budget-manager
pip install -r requirements.txt
```

## Usage

```bash
python3 project.py
```

Add transactions, set budget limits on any expense category, and check the Monthly Summary to see spending vs. budget for the month.

## Running Tests

```bash
pytest test_project.py -v
```

The test suite covers:
- Transaction validation (type, positive amount, non-empty category) and unique ID assignment
- Editing a transaction, including the type/category consistency safeguard
- Filtering by type, category, and search term
- Balance calculation
- Budget comparison logic (`is_over_budget`) at and around the limit
- Category spending totals restricted to a specific month vs. all-time
- **Monthly summary correctly reflects budget status per category** — spent, limit, remaining, and over-budget flag
- Real-time budget alert messages: triggered when over budget, silent when under or when no limit is set
- Category and budget file persistence, including a malformed categories file falling back to defaults, and a budget-limits file with one bad line not losing the other valid entries

## Design Notes

The program separates **pure logic** from **I/O**. Nothing except `load_transactions`/`save_transactions`/`load_categories`/`save_categories`/`load_category_budgets`/`save_category_budget` touches disk — every calculation, filter, and comparison is a plain function that takes data in and returns data out.

| Function | Responsibility |
|---|---|
| `add_transaction` / `edit_transaction` | Pure — validate and apply changes, return a new list |
| `filter_transactions` | Pure — powers all view/search options |
| `get_balance` | Pure — total income/expense/net |
| `get_monthly_summary` | Pure — **the core of the budget-in-summary feature**: aggregates by month and category, attaches budget status to each |
| `is_over_budget` / `get_category_spent` / `get_budget_alert_message` | Pure — budget comparison logic, shared between the summary view and the real-time alert |
| `format_table` / `format_transactions_table` / `format_balance` / `format_monthly_summary` | Pure — turn data into display strings |
| `load_categories` / `save_categories` | I/O — with fallback to defaults on a missing or malformed file |
| `load_category_budgets` / `save_category_budget` | I/O — skips individually malformed lines instead of losing the whole file |
| `main()` | Top-level menu loop |

### How the budget-in-summary feature works

Budget limits (set via option 8) are a single value per category — e.g., "Food: $250" — not tied to any particular month. `get_monthly_summary` treats this as a **recurring monthly cap**: for each month found in your transaction history, it sums that month's spending per category and compares it against the category's limit, marking it `OVER BUDGET` if that month's spending alone exceeded it. This means the same $250 Food limit is checked fresh against every month's spending, which is what "budget" conventionally means in personal finance (a monthly allowance, not a one-time total).

### Two bugs fixed from the original version

1. **`load_categories` could silently return two empty lists** if the categories file existed but had no recognizable `[INCOME]`/`[EXPENSE]` markers — which would make adding any transaction impossible (nothing to select from). It now falls back to sensible defaults in that case.
2. **Editing a transaction's type didn't check that its category still made sense** — e.g., changing `type` from `expense` to `income` without also changing `category` away from `Food`. `edit_transaction` now rejects this combination unless a valid new category is provided alongside the type change.

## Possible Improvements

- Recurring/scheduled transactions (e.g., monthly rent auto-logged)
- Export monthly summaries to CSV or PDF
- Multi-currency support
- Yearly summary view, not just monthly
- Category-level historical trend charts

## License

Part of the [Python Project Portfolio](https://github.com/contactsivaranjaniwork-netizen/Python-Projects) — see the root LICENSE file.
