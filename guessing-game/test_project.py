import pytest
from project import (
    get_difficulty_settings,
    check_guess,
    is_valid_guess,
    update_stats,
    load_stats,
    save_stats,
    format_stats,
)


def test_get_difficulty_settings():
    assert get_difficulty_settings("easy") == (1, 50, 10)
    assert get_difficulty_settings("Medium") == (1, 100, 7)  # case-insensitive
    assert get_difficulty_settings("HARD") == (1, 200, 5)

    with pytest.raises(ValueError):
        get_difficulty_settings("nightmare")


def test_check_guess():
    assert check_guess(50, 25) == "too_low"
    assert check_guess(50, 75) == "too_high"
    assert check_guess(50, 50) == "correct"


def test_is_valid_guess():
    assert is_valid_guess("42", 1, 100) == 42
    assert is_valid_guess("1", 1, 100) == 1
    assert is_valid_guess("100", 1, 100) == 100

    with pytest.raises(ValueError):
        is_valid_guess("abc", 1, 100)
    with pytest.raises(ValueError):
        is_valid_guess("101", 1, 100)  # above range
    with pytest.raises(ValueError):
        is_valid_guess("0", 1, 100)  # below range
    with pytest.raises(ValueError):
        is_valid_guess("4.5", 1, 100)  # not a whole number


def test_update_stats_tracks_wins_and_losses():
    stats = {"games_played": 0, "difficulties": {}}

    update_stats(stats, "easy", won=True, guesses_used=4)
    assert stats["games_played"] == 1
    assert stats["difficulties"]["easy"]["games_played"] == 1
    assert stats["difficulties"]["easy"]["wins"] == 1
    assert stats["difficulties"]["easy"]["losses"] == 0
    assert stats["difficulties"]["easy"]["best_guesses"] == 4

    update_stats(stats, "easy", won=False, guesses_used=10)
    assert stats["difficulties"]["easy"]["games_played"] == 2
    assert stats["difficulties"]["easy"]["losses"] == 1
    assert stats["difficulties"]["easy"]["best_guesses"] == 4  # unchanged by a loss


def test_update_stats_only_replaces_best_when_strictly_better():
    stats = {"games_played": 0, "difficulties": {}}

    update_stats(stats, "medium", won=True, guesses_used=5)
    assert stats["difficulties"]["medium"]["best_guesses"] == 5

    # Worse result -> best_guesses must NOT change
    update_stats(stats, "medium", won=True, guesses_used=7)
    assert stats["difficulties"]["medium"]["best_guesses"] == 5

    # Better result -> best_guesses SHOULD update
    update_stats(stats, "medium", won=True, guesses_used=3)
    assert stats["difficulties"]["medium"]["best_guesses"] == 3

    # Equal result -> stays the same (not strictly better)
    update_stats(stats, "medium", won=True, guesses_used=3)
    assert stats["difficulties"]["medium"]["best_guesses"] == 3


def test_load_and_save_stats(tmp_path):
    stats_file = tmp_path / "stats.json"

    assert load_stats(stats_file) == {"games_played": 0, "difficulties": {}}

    stats = {"games_played": 0, "difficulties": {}}
    update_stats(stats, "hard", won=True, guesses_used=2)
    save_stats(stats, stats_file)

    loaded = load_stats(stats_file)
    assert loaded["games_played"] == 1
    assert loaded["difficulties"]["hard"]["best_guesses"] == 2


def test_load_stats_handles_corrupted_file(tmp_path):
    stats_file = tmp_path / "bad_stats.json"
    stats_file.write_text("{not valid json")

    assert load_stats(stats_file) == {"games_played": 0, "difficulties": {}}


def test_format_stats():
    assert format_stats({"games_played": 0, "difficulties": {}}) == "No games played yet."

    stats = {"games_played": 0, "difficulties": {}}
    update_stats(stats, "easy", won=True, guesses_used=5)
    update_stats(stats, "easy", won=False, guesses_used=10)

    formatted = format_stats(stats)
    assert "Total games played: 2" in formatted
    assert "Easy" in formatted
    assert "Best: 5" in formatted