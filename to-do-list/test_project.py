import pytest
from project import (
    add_task,
    get_task_by_id,
    edit_task,
    toggle_task_complete,
    delete_task,
    format_task_list,
    load_tasks,
    save_tasks,
)


def make_sample_tasks():
    tasks = []
    tasks = add_task(tasks, "Buy milk", "2% milk", "Low")
    tasks = add_task(tasks, "Finish CS50P project", "Wrap up final project", "High")
    return tasks


def test_add_task_assigns_unique_id_and_preserves_existing():
    tasks = add_task([], "First task")
    assert len(tasks) == 1
    assert tasks[0]["id"] == 1
    assert tasks[0]["name"] == "First task"
    assert tasks[0]["completed"] is False

    tasks = add_task(tasks, "Second task")
    assert len(tasks) == 2
    assert tasks[1]["id"] == 2
    # Original first task must still be present and unchanged
    assert tasks[0]["name"] == "First task"


def test_add_task_rejects_empty_name():
    with pytest.raises(ValueError):
        add_task([], "")
    with pytest.raises(ValueError):
        add_task([], "   ")


def test_add_task_does_not_mutate_input_list():
    original = []
    add_task(original, "Some task")
    assert original == []  # original list untouched


def test_get_task_by_id():
    tasks = make_sample_tasks()
    task = get_task_by_id(tasks, 1)
    assert task["name"] == "Buy milk"
    assert get_task_by_id(tasks, 999) is None


def test_edit_task():
    tasks = make_sample_tasks()
    updated = edit_task(tasks, 1, {"name": "Buy oat milk", "priority": "Medium"})

    edited_task = get_task_by_id(updated, 1)
    assert edited_task["name"] == "Buy oat milk"
    assert edited_task["priority"] == "Medium"
    # Other task untouched
    assert get_task_by_id(updated, 2)["name"] == "Finish CS50P project"

    with pytest.raises(ValueError):
        edit_task(tasks, 999, {"name": "Doesn't exist"})


def test_toggle_task_complete():
    tasks = make_sample_tasks()
    assert get_task_by_id(tasks, 1)["completed"] is False

    tasks = toggle_task_complete(tasks, 1)
    assert get_task_by_id(tasks, 1)["completed"] is True

    tasks = toggle_task_complete(tasks, 1)
    assert get_task_by_id(tasks, 1)["completed"] is False

    with pytest.raises(ValueError):
        toggle_task_complete(tasks, 999)


def test_delete_task():
    tasks = make_sample_tasks()
    updated = delete_task(tasks, 1)

    assert len(updated) == 1
    assert get_task_by_id(updated, 1) is None
    assert get_task_by_id(updated, 2) is not None

    with pytest.raises(ValueError):
        delete_task(tasks, 999)


def test_format_task_list():
    assert format_task_list([]) == "No tasks yet. Add one first!"

    tasks = make_sample_tasks()
    formatted = format_task_list(tasks)
    assert "Buy milk" in formatted
    assert "Finish CS50P project" in formatted
    assert "[ ] Pending" in formatted

    tasks = toggle_task_complete(tasks, 1)
    formatted = format_task_list(tasks)
    assert "[x] Done" in formatted


def test_load_and_save_tasks(tmp_path):
    filepath = tmp_path / "todo.json"

    assert load_tasks(filepath) == []

    tasks = add_task([], "Persisted task")
    save_tasks(tasks, filepath)

    loaded = load_tasks(filepath)
    assert len(loaded) == 1
    assert loaded[0]["name"] == "Persisted task"


def test_load_tasks_handles_corrupted_file(tmp_path):
    filepath = tmp_path / "bad_todo.json"
    filepath.write_text("{not valid json")

    assert load_tasks(filepath) == []