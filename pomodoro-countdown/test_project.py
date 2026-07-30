import pytest
from project import (
    format_time,
    build_pomodoro_sequence,
    log_session,
    read_history,
    get_session_summary,
    format_summary,
    load_settings,
    save_settings,
    DEFAULT_SETTINGS,
)


def test_format_time():
    assert format_time(90) == "01:30"
    assert format_time(0) == "00:00"
    assert format_time(3661) == "61:01"  # minutes aren't capped at 59


def test_build_pomodoro_sequence_order_and_count():
    sequence = build_pomodoro_sequence(
        work_min=25, short_break_min=5, long_break_min=15,
        cycles_before_long_break=4, total_cycles=4,
    )
    # 4 work sessions, each followed by a break -> 8 intervals total
    assert len(sequence) == 8

    labels = [label for label, _, _ in sequence]
    assert labels == [
        "Work Session 1", "Short Break",
        "Work Session 2", "Short Break",
        "Work Session 3", "Short Break",
        "Work Session 4", "Long Break",
    ]

    # The 4th break (after the 4th work session) must be the long break
    assert sequence[-1] == ("Long Break", "Long Break", 15)
    assert sequence[1] == ("Short Break", "Short Break", 5)


def test_build_pomodoro_sequence_invalid_input():
    with pytest.raises(ValueError):
        build_pomodoro_sequence(25, 5, 15, 4, 0)  # zero cycles requested
    with pytest.raises(ValueError):
        build_pomodoro_sequence(0, 5, 15, 4, 4)  # invalid work duration
    with pytest.raises(ValueError):
        build_pomodoro_sequence(25, 5, 15, 0, 4)  # invalid cycles_before_long_break


def test_log_session_and_read_history(tmp_path):
    log_file = tmp_path / "history.csv"

    assert read_history(log_file) == []

    log_session("Work", 25, log_file=log_file)
    log_session("Short Break", 5, log_file=log_file)

    history = read_history(log_file)
    assert len(history) == 2
    assert history[0]["Type"] == "Work"
    assert history[0]["Duration_Mins"] == "25"
    assert history[1]["Type"] == "Short Break"


def test_get_session_summary_and_format():
    history = [
        {"Timestamp": "29-07-2026 10:00:00", "Type": "Work", "Duration_Mins": "25"},
        {"Timestamp": "29-07-2026 10:30:00", "Type": "Work", "Duration_Mins": "25"},
        {"Timestamp": "29-07-2026 11:00:00", "Type": "Short Break", "Duration_Mins": "5"},
        {"Timestamp": "28-07-2026 09:00:00", "Type": "Work", "Duration_Mins": "25"},  # different day
    ]

    count, total_minutes = get_session_summary(history, date_str="29-07-2026")
    assert count == 2
    assert total_minutes == 50
    assert format_summary(count, total_minutes) == "Today: 2 work session(s) completed, 50 minutes focused."

    # No sessions for a date with no entries
    count, total_minutes = get_session_summary(history, date_str="01-01-2020")
    assert count == 0
    assert total_minutes == 0
    assert format_summary(count, total_minutes) == "No work sessions recorded for today yet."


def test_load_and_save_settings(tmp_path):
    config_file = tmp_path / "settings.json"

    # No file yet -> defaults
    assert load_settings(config_file) == DEFAULT_SETTINGS

    custom = dict(DEFAULT_SETTINGS)
    custom["work_min"] = 50
    save_settings(custom, config_file)

    loaded = load_settings(config_file)
    assert loaded["work_min"] == 50
    assert loaded["short_break_min"] == DEFAULT_SETTINGS["short_break_min"]


def test_load_settings_handles_corrupted_file(tmp_path):
    config_file = tmp_path / "bad_settings.json"
    config_file.write_text("{not valid json")

    assert load_settings(config_file) == DEFAULT_SETTINGS