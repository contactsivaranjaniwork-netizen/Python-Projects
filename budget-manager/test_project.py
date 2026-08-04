import pytest
from project import (
    validate_txn_type,
    add_transaction,
    get_transaction_by_id,
    edit_transaction,
    filter_transactions,
    get_balance,
    is_over_budget,
    get_category_spent,
    get_monthly_summary,
    get_budget_alert_message,
    get_unique_categories,
    format_table,
    format_transactions_table,
    format_balance,
    format_monthly_summary,
    load_transactions,
    save_transactions,
    load_categories,
    save_categories,
    load_category_budgets,
    save_category_budget,
    DEFAULT_INCOME_CATS,
    DEFAULT_EXPENSE_CATS,
)


def make_sample_transactions():
    transactions = []
    transactions = add_transaction(transactions, "income", 2000, "Salary", "August pay")
    transactions = add_transaction(transactions, "expense", 300, "Food", "Groceries")
    transactions = add_transaction(transactions, "expense", 150, "Food", "Restaurants")
    transactions = add_transaction(transactions, "expense", 800, "Rent", "August rent")
    return transactions


def test_validate_txn_type():
    assert validate_txn_type("income") == "income"
    assert validate_txn_type("EXPENSE") == "expense"
    assert validate_txn_type("  income  ") == "income"
    assert validate_txn_type("savings") is None


def test_add_transaction_assigns_id_and_validates():
    transactions = add_transaction([], "income", 100, "Salary")
    assert len(transactions) == 1
    assert transactions[0]["transaction_id"] == 1
    assert transactions[0]["type"] == "income"
    assert transactions[0]["amount"] == 100

    transactions = add_transaction(transactions, "expense", 50, "Food")
    assert transactions[1]["transaction_id"] == 2

    with pytest.raises(ValueError):
        add_transaction([], "savings", 100, "Salary")  # invalid type
    with pytest.raises(ValueError):
        add_transaction([], "income", 0, "Salary")  # non-positive amount
    with pytest.raises(ValueError):
        add_transaction([], "income", 100, "")  # empty category


def test_add_transaction_does_not_mutate_input():
    original = []
    add_transaction(original, "income", 100, "Salary")
    assert original == []


def test_edit_transaction():
    transactions = make_sample_transactions()

    updated = edit_transaction(transactions, 2, {"amount": 275.0})
    assert get_transaction_by_id(updated, 2)["amount"] == 275.0
    # Other transactions untouched
    assert get_transaction_by_id(updated, 1)["amount"] == 2000

    with pytest.raises(ValueError):
        edit_transaction(transactions, 999, {"amount": 10})


def test_edit_transaction_rejects_type_category_mismatch():
    transactions = make_sample_transactions()
    valid_categories = {"income": DEFAULT_INCOME_CATS, "expense": DEFAULT_EXPENSE_CATS}

    # Changing type to 'income' without updating category='Food' should be rejected
    with pytest.raises(ValueError):
        edit_transaction(transactions, 2, {"type": "income"}, valid_categories)

    # Changing both type AND category consistently should succeed
    updated = edit_transaction(transactions, 2, {"type": "income", "category": "Salary"}, valid_categories)
    assert get_transaction_by_id(updated, 2)["type"] == "income"
    assert get_transaction_by_id(updated, 2)["category"] == "Salary"


def test_filter_transactions():
    transactions = make_sample_transactions()

    income_only = filter_transactions(transactions, tx_type="income")
    assert len(income_only) == 1
    assert income_only[0]["category"] == "Salary"

    food_only = filter_transactions(transactions, category="food")  # case-insensitive
    assert len(food_only) == 2

    searched = filter_transactions(transactions, search="rent")
    assert len(searched) == 1
    assert searched[0]["category"] == "Rent"


def test_get_balance():
    transactions = make_sample_transactions()
    income, expense, net = get_balance(transactions)
    assert income == 2000
    assert expense == 300 + 150 + 800
    assert net == income - expense


def test_is_over_budget():
    assert is_over_budget(600, 500) is True
    assert is_over_budget(400, 500) is False
    assert is_over_budget(600, None) is False  # no limit set -> never over


def test_get_category_spent_respects_month_filter():
    transactions = make_sample_transactions()
    # All sample transactions were just created "now", so they share a month
    from project import get_current_month
    this_month = get_current_month()

    spent_this_month = get_category_spent(transactions, "Food", month=this_month)
    assert spent_this_month == 450  # 300 + 150

    spent_other_month = get_category_spent(transactions, "Food", month="2000-01")
    assert spent_other_month == 0

    spent_all_time = get_category_spent(transactions, "Food", month=None)
    assert spent_all_time == 450


def test_get_monthly_summary_reflects_budget():
    transactions = make_sample_transactions()
    from project import get_current_month
    this_month = get_current_month()

    budgets = {"food": 400.0}  # Food is over budget (450 spent), Rent has no limit
    summary = get_monthly_summary(transactions, budgets)

    assert this_month in summary
    month_data = summary[this_month]
    assert month_data["income"] == 2000
    assert month_data["expense"] == 1250

    food_info = month_data["categories"]["Food"]
    assert food_info["spent"] == 450
    assert food_info["limit"] == 400.0
    assert food_info["over_budget"] is True
    assert food_info["remaining"] == pytest.approx(-50.0)

    rent_info = month_data["categories"]["Rent"]
    assert rent_info["limit"] is None
    assert rent_info["over_budget"] is False


def test_get_budget_alert_message():
    transactions = make_sample_transactions()
    from project import get_current_month
    this_month = get_current_month()

    # Under budget -> no alert
    budgets = {"food": 1000.0}
    assert get_budget_alert_message(transactions, "Food", budgets, month=this_month) is None

    # Over budget -> alert message returned
    budgets = {"food": 400.0}
    alert = get_budget_alert_message(transactions, "Food", budgets, month=this_month)
    assert alert is not None
    assert "Food" in alert
    assert "exceeded" in alert

    # No limit set at all -> no alert
    budgets = {}
    assert get_budget_alert_message(transactions, "Food", budgets, month=this_month) is None


def test_get_unique_categories():
    transactions = make_sample_transactions()
    income_cats, expense_cats = get_unique_categories(transactions)
    assert income_cats == ["Salary"]
    assert expense_cats == ["Food", "Rent"]


def test_format_table():
    assert format_table([], ["A", "B"]) == "Empty dataset."
    formatted = format_table([["1", "hello"]], ["ID", "Name"])
    assert "ID" in formatted and "hello" in formatted


def test_format_transactions_table_and_balance():
    transactions = make_sample_transactions()
    table = format_transactions_table(transactions)
    assert "Salary" in table
    assert "Food" in table

    balance_text = format_balance(2000, 1250, 750)
    assert "$2000.00" in balance_text
    assert "$750.00" in balance_text


def test_format_monthly_summary_shows_budget_status():
    transactions = make_sample_transactions()
    budgets = {"food": 400.0}
    summary = get_monthly_summary(transactions, budgets)
    formatted = format_monthly_summary(summary)

    assert "OVER BUDGET" in formatted
    assert "Food" in formatted
    assert "no budget set" in formatted  # Rent has no limit


def test_load_and_save_transactions(tmp_path):
    filepath = tmp_path / "budget.csv"

    assert load_transactions(filepath) == []

    transactions = add_transaction([], "income", 500, "Salary")
    save_transactions(transactions, filepath)

    loaded = load_transactions(filepath)
    assert len(loaded) == 1
    assert loaded[0]["amount"] == 500.0
    assert loaded[0]["type"] == "income"


def test_load_categories_creates_default_file(tmp_path):
    filepath = tmp_path / "categories.txt"
    assert not filepath.exists()

    income, expense = load_categories(filepath)
    assert filepath.exists()
    assert income == DEFAULT_INCOME_CATS
    assert expense == DEFAULT_EXPENSE_CATS


def test_load_categories_falls_back_on_malformed_file(tmp_path):
    filepath = tmp_path / "bad_categories.txt"
    filepath.write_text("just some random text\nwith no markers at all\n")

    income, expense = load_categories(filepath)
    assert income == DEFAULT_INCOME_CATS
    assert expense == DEFAULT_EXPENSE_CATS


def test_save_and_load_categories_roundtrip(tmp_path):
    filepath = tmp_path / "categories.txt"
    save_categories(["Salary", "Bonus"], ["Food", "Rent"], filepath)

    income, expense = load_categories(filepath)
    assert income == ["Bonus", "Salary"]  # saved sorted
    assert expense == ["Food", "Rent"]


def test_load_category_budgets_skips_bad_lines_but_keeps_good_ones(tmp_path):
    filepath = tmp_path / "budgets.txt"
    filepath.write_text("food:400\nrent:not_a_number\nutilities:150\n")

    limits = load_category_budgets(filepath)
    assert limits == {"food": 400.0, "utilities": 150.0}
    assert "rent" not in limits  # bad line skipped, doesn't kill the rest


def test_save_category_budget(tmp_path):
    filepath = tmp_path / "budgets.txt"
    save_category_budget("Food", 500, filepath)
    save_category_budget("Rent", 1200, filepath)

    limits = load_category_budgets(filepath)
    assert limits == {"food": 500.0, "rent": 1200.0}

    with pytest.raises(ValueError):
        save_category_budget("Food", -10, filepath)