import string
import pytest
from project import (
    build_character_pool,
    generate_password,
    check_password_strength,
    log_generation,
    read_log,
    format_log,
)


def test_build_character_pool():
    assert build_character_pool(True, False, False, False) == string.ascii_uppercase
    pool = build_character_pool(True, True, True, True)
    assert set(pool) == set(
        string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    )

    with pytest.raises(ValueError):
        build_character_pool(False, False, False, False)


def test_generate_password_length_and_charset():
    password = generate_password(16, True, True, True, True)
    assert len(password) == 16
    allowed = set(
        string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    )
    assert all(char in allowed for char in password)


def test_generate_password_contains_all_selected_sets():
    # Run many times since generation is random; construction guarantees
    # this every single time, so a handful of runs is enough to catch a regression.
    for _ in range(50):
        password = generate_password(12, True, True, True, True)
        assert any(c in string.ascii_uppercase for c in password)
        assert any(c in string.ascii_lowercase for c in password)
        assert any(c in string.digits for c in password)
        assert any(c in string.punctuation for c in password)


def test_generate_password_only_uses_selected_sets():
    # Only digits selected -> password must be all digits
    for _ in range(20):
        password = generate_password(10, False, False, True, False)
        assert all(char in string.digits for char in password)


def test_generate_password_invalid_input():
    with pytest.raises(ValueError):
        generate_password(3, True, False, False, False)  # below MIN_LENGTH

    with pytest.raises(ValueError):
        generate_password(200, True, False, False, False)  # above MAX_LENGTH

    with pytest.raises(ValueError):
        generate_password(10, False, False, False, False)  # no character set selected

    with pytest.raises(ValueError):
        # length 3 can't fit one character from each of 4 required sets
        generate_password(3, True, True, True, True)

    # Exactly at the minimum needed for 4 required sets should succeed, not raise
    assert len(generate_password(4, True, True, True, True)) == 4


def test_check_password_strength():
    assert check_password_strength("abc") == "Weak"
    assert check_password_strength("abcdefgh") == "Moderate"  # 8 chars, lowercase only -> len<=12,charset=1
    assert check_password_strength("Abcdefgh1") == "Strong"  # 9 chars, 3 sets (upper/lower/digit)
    assert check_password_strength("Ab1!Ab1!Ab1!") == "Strong"  # 12 chars, all 4 sets
    assert check_password_strength("Ab1!Ab1!Ab1!Ab1!") == "Strong"  # >12 chars, all 4 sets

    with pytest.raises(ValueError):
        check_password_strength("")


def test_log_and_read_and_format(tmp_path):
    log_file = tmp_path / "log.json"

    assert read_log(log_file) == []
    assert format_log(read_log(log_file)) == "No history found."

    log_generation(16, True, True, True, True, log_file=log_file)
    log_generation(8, True, False, True, False, log_file=log_file)

    log = read_log(log_file)
    assert len(log) == 2
    assert log[0]["length"] == 16
    assert log[1]["upper"] is True
    assert log[1]["lower"] is False

    formatted = format_log(log)
    assert "Length: 16" in formatted
    assert "Length: 8" in formatted
