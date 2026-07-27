import pytest
from project import calculate, format_expression, log_calculation, read_history


def test_calculate_basic_operations():
    assert calculate(5, 3, "add") == 8
    assert calculate(5, 3, "subtract") == 2
    assert calculate(5, 3, "multiply") == 15
    assert calculate(6, 3, "divide") == 2
    assert calculate(7, 3, "modulus") == 1
    assert calculate(2, 3, "exponent") == 8
    assert calculate(7, 2, "floor_divide") == 3

    # Works with floats too
    assert calculate(5.5, 2, "add") == pytest.approx(7.5)
    assert calculate(7, 2, "divide") == pytest.approx(3.5)


def test_calculate_zero_division_errors():
    with pytest.raises(ZeroDivisionError):
        calculate(5, 0, "divide")
    with pytest.raises(ZeroDivisionError):
        calculate(5, 0, "modulus")
    with pytest.raises(ZeroDivisionError):
        calculate(5, 0, "floor_divide")
    # 0 raised to a negative power is undefined
    with pytest.raises(ZeroDivisionError):
        calculate(0, -1, "exponent")


def test_calculate_invalid_operation():
    with pytest.raises(ValueError):
        calculate(5, 3, "square_root")


def test_format_expression():
    assert format_expression(5, 3, "+", 8) == "5 + 3 = 8"
    assert format_expression(7, 2, "/", 3.5) == "7 / 2 = 3.5"


def test_log_and_read_history(tmp_path):
    filepath = tmp_path / "history.txt"

    # No file yet -> empty history
    assert read_history(filepath) == []

    log_calculation("5 + 3 = 8", filepath=filepath)
    log_calculation("7 / 2 = 3.5", filepath=filepath)

    history = read_history(filepath)
    assert len(history) == 2
    assert "5 + 3 = 8" in history[0]
    assert "7 / 2 = 3.5" in history[1]
    # Each entry should include a timestamp in brackets
    assert history[0].startswith("[")