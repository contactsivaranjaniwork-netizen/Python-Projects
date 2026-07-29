import json
import pytest
from project import (
    generate_qr_code,
    build_filename,
    log_generation,
    read_history,
    format_history,
)


def test_generate_qr_code_creates_file(tmp_path):
    filepath = tmp_path / "test_qr.png"
    result = generate_qr_code("https://example.com", filepath)

    assert filepath.exists()
    assert result == str(filepath)


def test_generate_qr_code_empty_text_raises(tmp_path):
    filepath = tmp_path / "test_qr.png"

    with pytest.raises(ValueError):
        generate_qr_code("", filepath)

    with pytest.raises(ValueError):
        generate_qr_code("   ", filepath)


def test_generate_qr_code_creates_missing_directory(tmp_path):
    nested_path = tmp_path / "nested" / "dir" / "qr.png"
    generate_qr_code("hello", nested_path)
    assert nested_path.exists()


def test_build_filename_unique_and_creates_dir(tmp_path):
    output_dir = tmp_path / "qr_output"
    path1 = build_filename(output_dir)
    path2 = build_filename(output_dir)

    assert output_dir.exists()
    assert path1 != path2
    assert path1.suffix == ".png"
    assert path1.parent == output_dir


def test_log_and_read_history(tmp_path):
    history_file = tmp_path / "history.json"

    # No file yet -> empty list
    assert read_history(history_file) == []

    log_generation("hello world", "qr_codes/qr_1.png", history_file=history_file)
    log_generation("https://example.com", "qr_codes/qr_2.png", history_file=history_file)

    history = read_history(history_file)
    assert len(history) == 2
    assert history[0]["original_text"] == "hello world"
    assert history[1]["filename"] == "qr_codes/qr_2.png"


def test_read_history_handles_corrupted_file(tmp_path):
    history_file = tmp_path / "bad_history.json"
    history_file.write_text("{not valid json")

    assert read_history(history_file) == []


def test_format_history():
    assert format_history([]) == "No QR codes generated yet."

    history = [
        {"timestamp": "01-01-2026 10:00:00", "original_text": "hello", "filename": "qr_1.png"},
    ]
    formatted = format_history(history)
    assert "hello" in formatted
    assert "qr_1.png" in formatted
    assert "Timestamp" in formatted