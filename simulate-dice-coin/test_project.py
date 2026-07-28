import pytest
from project import (
    roll_dice,
    flip_coins,
    update_stats,
    get_stats_summary,
    format_dice_summary,
    format_coin_summary,
    reset_stats,
)


def test_roll_dice():
    rolls = roll_dice(5, 6)
    assert len(rolls) == 5
    assert all(1 <= r <= 6 for r in rolls)

    # Invalid num_dice / sides raise ValueError
    with pytest.raises(ValueError):
        roll_dice(0, 6)
    with pytest.raises(ValueError):
        roll_dice(-1, 6)
    with pytest.raises(ValueError):
        roll_dice(3, 1)


def test_flip_coins():
    flips = flip_coins(10)
    assert len(flips) == 10
    assert all(f in ("Heads", "Tails") for f in flips)

    with pytest.raises(ValueError):
        flip_coins(0)
    with pytest.raises(ValueError):
        flip_coins(-5)


def test_update_stats():
    stats = {}
    update_stats(stats, [1, 2, 2, 3])
    assert stats == {1: 1, 2: 2, 3: 1}

    # Accumulates across multiple calls
    update_stats(stats, [2, 4])
    assert stats == {1: 1, 2: 3, 3: 1, 4: 1}


def test_get_stats_summary():
    # Empty stats
    total, breakdown = get_stats_summary({})
    assert total == 0
    assert breakdown == []

    stats = {1: 2, 2: 2}
    total, breakdown = get_stats_summary(stats)
    assert total == 4
    assert breakdown == [(1, 2, 50.0), (2, 2, 50.0)]


def test_format_summaries():
    assert format_dice_summary({}) == "No dice rolls yet."
    assert format_coin_summary({}) == "No coin flips yet."

    dice_summary = format_dice_summary({6: 2, 3: 2})
    assert "Total Rolls: 4" in dice_summary
    assert "Side 3: 2 (50.0%)" in dice_summary
    assert "Side 6: 2 (50.0%)" in dice_summary

    coin_summary = format_coin_summary({"Heads": 3, "Tails": 1})
    assert "Total Flips: 4" in coin_summary
    assert "Heads: 3 (75.0%)" in coin_summary
    assert "Tails: 1 (25.0%)" in coin_summary


def test_reset_stats():
    dice_stats = {1: 3, 2: 5}
    coin_stats = {"Heads": 4}
    reset_stats(dice_stats, coin_stats)
    assert dice_stats == {}
    assert coin_stats == {}