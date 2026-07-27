import pytest
from project import get_categories, get_random_quote, add_quote, format_quote


SAMPLE_QUOTES = [
    {"text": "Quote A", "author": "Author A", "category": "motivation"},
    {"text": "Quote B", "author": "Author B", "category": "humor"},
    {"text": "Quote C", "author": "", "category": "motivation"},
]


def test_get_categories():
    assert get_categories(SAMPLE_QUOTES) == ["humor", "motivation"]
    assert get_categories([]) == []
    # Quotes missing a "category" key should be ignored, not crash
    assert get_categories([{"text": "no category"}]) == []


def test_get_random_quote():
    # With no category, result must be one of the full list
    result = get_random_quote(SAMPLE_QUOTES)
    assert result in SAMPLE_QUOTES

    # Filtered by category, result must belong to that category
    result = get_random_quote(SAMPLE_QUOTES, category="motivation")
    assert result["category"] == "motivation"

    # Empty list returns None instead of raising
    assert get_random_quote([]) is None

    # Category with no matches returns None
    assert get_random_quote(SAMPLE_QUOTES, category="nonexistent") is None


def test_add_quote():
    updated = add_quote(SAMPLE_QUOTES, "New quote", "New Author", "affirmation")

    # Original list must not be mutated
    assert len(SAMPLE_QUOTES) == 3
    # New list has one more entry
    assert len(updated) == 4
    assert updated[-1] == {"text": "New quote", "author": "New Author", "category": "affirmation"}

    # Blank author/category default correctly
    updated2 = add_quote(SAMPLE_QUOTES, "Another quote", "", "")
    assert updated2[-1]["author"] == "Unknown"
    assert updated2[-1]["category"] == "general"

    # Empty text raises ValueError
    with pytest.raises(ValueError):
        add_quote(SAMPLE_QUOTES, "   ", "Author", "category")


def test_format_quote():
    quote = {"text": "Hello world", "author": "Author A"}
    assert format_quote(quote) == '"Hello world"\n\n— Author A'

    # Missing/blank author defaults to Unknown
    quote_no_author = {"text": "Hello again", "author": ""}
    assert format_quote(quote_no_author) == '"Hello again"\n\n— Unknown'