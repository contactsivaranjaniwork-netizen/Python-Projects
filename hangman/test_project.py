import pytest
from project import (
    choose_word,
    get_display_word,
    process_guess,
    is_game_won,
    is_game_lost,
    load_words,
    load_stats,
    save_stats,
    DEFAULT_STATS,
)


SAMPLE_BANK = {
    "Animals": {"Easy": ["cat", "dog"], "Hard": ["elephant"]},
    "Movies": {"Easy": ["jaws"], "Hard": ["inception"]},
}


def test_choose_word_respects_category_and_difficulty():
    word = choose_word(SAMPLE_BANK, category="Animals", difficulty="Easy")
    assert word in ["cat", "dog"]

    word = choose_word(SAMPLE_BANK, category="Movies", difficulty="Hard")
    assert word == "inception"


def test_choose_word_falls_back_on_invalid_category():
    # Category doesn't exist -> falls back to a random valid one, still returns a real word
    word = choose_word(SAMPLE_BANK, category="Nonexistent", difficulty="Easy")
    all_words = [w for cat in SAMPLE_BANK.values() for words in cat.values() for w in words]
    assert word in all_words


def test_get_display_word():
    assert get_display_word("cat", set()) == "_ _ _"
    assert get_display_word("cat", {"c"}) == "c _ _"
    assert get_display_word("cat", {"c", "a", "t"}) == "c a t"
    assert get_display_word("cat", {"x", "y"}) == "_ _ _"


def test_process_guess_correct_and_incorrect():
    guessed = set()
    wrong = set()

    status = process_guess("cat", "c", guessed, wrong)
    assert status == "correct"
    assert "c" in guessed
    assert wrong == set()

    status = process_guess("cat", "z", guessed, wrong)
    assert status == "incorrect"
    assert "z" in wrong
    assert "c" in guessed  # unaffected


def test_process_guess_repeat():
    guessed = {"c"}
    wrong = {"z"}

    assert process_guess("cat", "c", guessed, wrong) == "repeat"
    assert process_guess("cat", "z", guessed, wrong) == "repeat"
    # Sets unchanged, no duplicate additions
    assert guessed == {"c"}
    assert wrong == {"z"}


def test_process_guess_invalid_input():
    guessed = set()
    wrong = set()

    for bad_guess in ["", "ab", "1", "!", "  "]:
        status = process_guess("cat", bad_guess, guessed, wrong)
        assert status == "invalid"

    # Invalid guesses must not mutate state or consume a turn
    assert guessed == set()
    assert wrong == set()


def test_is_game_won():
    assert is_game_won("cat", {"c", "a", "t"}) is True
    assert is_game_won("cat", {"c", "a"}) is False
    assert is_game_won("cat", set()) is False


def test_is_game_lost():
    assert is_game_lost(set(), max_wrong=7) is False
    assert is_game_lost({"a", "b", "c", "d", "e", "f"}, max_wrong=7) is False
    assert is_game_lost({"a", "b", "c", "d", "e", "f", "g"}, max_wrong=7) is True  # exact boundary
    assert is_game_lost({"a", "b", "c", "d", "e", "f", "g", "h"}, max_wrong=7) is True


def test_load_and_save_stats(tmp_path):
    stats_file = tmp_path / "stats.json"

    assert load_stats(stats_file) == DEFAULT_STATS

    custom = {"games_played": 5, "wins": 3, "losses": 2}
    save_stats(custom, stats_file)

    assert load_stats(stats_file) == custom


def test_load_stats_handles_corrupted_file(tmp_path):
    stats_file = tmp_path / "bad_stats.json"
    stats_file.write_text("{not valid json")

    assert load_stats(stats_file) == DEFAULT_STATS


def test_load_words_creates_default_file(tmp_path):
    word_file = tmp_path / "words.json"

    assert not word_file.exists()
    bank = load_words(word_file)

    assert word_file.exists()
    assert "General" in bank


def test_load_words_handles_corrupted_file(tmp_path):
    word_file = tmp_path / "bad_words.json"
    word_file.write_text("{not valid json")

    bank = load_words(word_file)
    assert "General" in bank