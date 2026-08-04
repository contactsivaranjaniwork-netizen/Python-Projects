# ✅ To-Do List Manager

A command-line to-do list manager with full CRUD support — add, edit, toggle-complete, and delete tasks — with the entire list persisted to a JSON file after every change.

## Features

- **Add tasks** — name, optional description, and priority (Low/Medium/High); each task gets a unique auto-incrementing ID.
- **View tasks** — numbered list with clear `[x] Done` / `[ ] Pending` status, priority, description, and creation timestamp.
- **Edit tasks** — update name, description, or priority via a submenu, by task ID.
- **Toggle complete/incomplete** — flip a task's status by ID, as its own dedicated menu option.
- **Delete tasks** — remove a task by ID, with a confirmation prompt before deleting.
- **Persistent storage** — every add/edit/toggle/delete immediately saves to `todo.json`, so nothing is lost if the program exits unexpectedly; tasks reload automatically on the next run.
- Invalid task IDs, non-numeric input, and empty task names are all caught and reported clearly instead of crashing.
- Core CRUD logic is fully separated from user input/output — every function operates on and returns a plain list, so it's independently unit-tested without touching any file.

## Demo

```
===== TO-DO LIST MANAGER =====
1. View Tasks
2. Add a Task
3. Edit a Task
4. Mark Task Complete / Incomplete
5. Delete a Task
6. Exit
===============================
Choose an option: 2
Enter task name: Finish CS50P final project
Enter task description (optional): Wrap up and submit
Enter priority (Low/Medium/High, default Medium): High

Task added!

Choose an option: 1

ID    Status     Name                 Priority   Description                              Created At
----------------------------------------------------------------------------------------------------
1     [ ] Pending Finish CS50P final p High       Wrap up and submit                       2026-08-03 07:56:52
```

## Project Structure

```
todo-list-manager/
├── project.py        # main program (menu loop + CRUD logic)
├── test_project.py    # pytest test suite
├── todo.json           # task list (created automatically)
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/contactsivaranjaniwork-netizen/Python-Projects.git
cd python-portfolio/to-do-list
pip install -r requirements.txt
```

## Usage

```bash
python3 project.py
```

View, add, edit, toggle, or delete tasks from the menu — every change is saved automatically.

## Running Tests

```bash
pytest test_project.py -v
```

The test suite covers:
- Adding a task assigns a correct, unique, incrementing ID and preserves all existing tasks
- Empty/whitespace-only task names are rejected with `ValueError`
- CRUD functions never mutate the list passed in — they return a new list
- Editing, toggling, and deleting a valid task ID work correctly, and each raises `ValueError` for an invalid ID
- `format_task_list` produces the expected display text, including the empty-list case
- Save/load round-trips correctly (using `pytest`'s `tmp_path`, so tests never touch your real `todo.json`), and a corrupted file falls back to an empty list

## Design Notes

The program separates **pure logic** from **I/O**, and every CRUD function is consistent: `tasks` is always the first parameter, and each one returns a new list rather than mutating its input.

| Function | Responsibility |
|---|---|
| `add_task(tasks, name, description, priority)` | Pure — validates name, assigns a new ID, returns a new list |
| `get_task_by_id(tasks, task_id)` | Pure — lookup, returns `None` if not found |
| `edit_task(tasks, task_id, updates)` | Pure — applies a dict of field updates, raises on invalid ID |
| `toggle_task_complete(tasks, task_id)` | Pure — flips completion status, raises on invalid ID |
| `delete_task(tasks, task_id)` | Pure — removes a task, raises on invalid ID |
| `format_task_list(tasks)` | Pure — formats the list for display |
| `load_tasks(filename)` / `save_tasks(tasks, filename)` | I/O — the ONLY functions that touch disk |
| `get_task_id_input(prompt)` | Input validation helper |
| `main()` | Top-level menu loop |

### Why this matters

An earlier version had every CRUD function open and write the file itself (`add_task`, `edit_task`, `delete_task` each did their own `load_tasks`/`json.dump`), with inconsistent parameter ordering across functions and duplicated (and inconsistent) corrupted-file handling between `load_tasks` and a separate `get_task_by_id`. Restructuring so **only** `load_tasks`/`save_tasks` touch disk — and every CRUD function operates purely on an in-memory list — is what makes each one testable with a plain Python list in milliseconds, with no file system involved at all.

## Possible Improvements

- Sort/filter tasks by priority, due date, or completion status
- Due-date support with overdue highlighting
- Undo support for the most recent delete
- Export the task list to a Markdown checklist
- Task categories/tags

## License

Part of the [Python Project Portfolio](../README.md) — see the root [LICENSE](../LICENSE) file.
