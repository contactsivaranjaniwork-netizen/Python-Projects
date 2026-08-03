"""
To-Do List Manager (CLI)
Add, edit, delete, and mark tasks complete; list is saved to and
reloaded from a file.

Structure:
- add_task / edit_task / toggle_task_complete / delete_task / get_task_by_id:
  pure, testable — operate on and return lists, never touch disk
- format_task_list: pure — formats a task list for display
- load_tasks / save_tasks: the ONLY functions that touch disk
- main: top-level menu loop
"""

import json
import os
from datetime import datetime

TODO_FILE = "todo.json"


def load_tasks(filename=TODO_FILE):
    """
    Load tasks from a JSON file.
    Returns an empty list if the file doesn't exist, is corrupted, or
    doesn't contain a list.
    """
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return []

    if not isinstance(data, list):
        return []

    return data


def save_tasks(tasks, filename=TODO_FILE):
    """Save the given list of tasks to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def add_task(tasks, name, description="", priority="Medium"):
    """
    Return a NEW list with a task appended (does not mutate the input list).
    Assigns a new unique ID (max existing ID + 1, or 1 if the list is empty).
    Raises ValueError if name is empty/whitespace-only.
    """
    name = name.strip()
    if not name:
        raise ValueError("Task name cannot be empty")

    new_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {
        "id": new_id,
        "name": name,
        "description": description.strip(),
        "completed": False,
        "priority": priority,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    return tasks + [new_task]


def get_task_by_id(tasks, task_id):
    """Return the task dict with the matching ID, or None if not found."""
    for task in tasks:
        if task.get("id") == task_id:
            return task
    return None


def edit_task(tasks, task_id, updates):
    """
    Return a NEW list with the matching task's fields updated according
    to the `updates` dict (e.g. {"name": "New name"}).
    Raises ValueError if task_id doesn't exist in tasks.
    """
    if get_task_by_id(tasks, task_id) is None:
        raise ValueError(f"No task found with ID {task_id}")

    return [
        {**task, **updates} if task.get("id") == task_id else task
        for task in tasks
    ]


def toggle_task_complete(tasks, task_id):
    """
    Return a NEW list with the matching task's completion status flipped.
    Raises ValueError if task_id doesn't exist in tasks.
    """
    task = get_task_by_id(tasks, task_id)
    if task is None:
        raise ValueError(f"No task found with ID {task_id}")

    return [
        {**t, "completed": not t["completed"]} if t.get("id") == task_id else t
        for t in tasks
    ]


def delete_task(tasks, task_id):
    """
    Return a NEW list with the matching task removed.
    Raises ValueError if task_id doesn't exist in tasks.
    """
    if get_task_by_id(tasks, task_id) is None:
        raise ValueError(f"No task found with ID {task_id}")

    return [task for task in tasks if task.get("id") != task_id]


def format_task_list(tasks):
    """Return a display-ready string listing all tasks."""
    if not tasks:
        return "No tasks yet. Add one first!"

    header = f"{'ID':<5} {'Status':<10} {'Name':<20} {'Priority':<10} {'Description':<40} {'Created At'}"
    separator = "-" * len(header)

    rows = [header, separator]
    for task in tasks:
        status = "[x] Done" if task["completed"] else "[ ] Pending"
        rows.append(
            f"{task['id']:<5} {status:<10} {task['name']:<20} "
            f"{task['priority']:<10} {task['description']:<40} {task['created_at']}"
        )

    return "\n".join(rows)


def get_task_id_input(prompt):
    """Repeatedly prompt until the user enters a valid integer task ID."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid numeric ID.")


def main():
    tasks = load_tasks()

    while True:
        print(
            "\n===== TO-DO LIST MANAGER =====\n"
            "1. View Tasks\n"
            "2. Add a Task\n"
            "3. Edit a Task\n"
            "4. Mark Task Complete / Incomplete\n"
            "5. Delete a Task\n"
            "6. Exit\n"
            "==============================="
        )
        choice = input("Choose an option: ")

        if choice == "1":
            print(f"\n{format_task_list(tasks)}")

        elif choice == "2":
            name = input("Enter task name: ")
            description = input("Enter task description (optional): ")
            priority = input("Enter priority (Low/Medium/High, default Medium): ").strip() or "Medium"
            try:
                tasks = add_task(tasks, name, description, priority)
                save_tasks(tasks)
                print("\nTask added!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            print(f"\n{format_task_list(tasks)}")
            task_id = get_task_id_input("Enter the ID of the task to edit: ")

            if get_task_by_id(tasks, task_id) is None:
                print("Task ID not found!")
                continue

            updates = {}
            while True:
                print(
                    "\n--- What do you want to edit? ---\n"
                    "1. Name\n"
                    "2. Description\n"
                    "3. Priority\n"
                    "4. Done editing"
                )
                edit_choice = input("Choose an option: ")

                if edit_choice == "1":
                    updates["name"] = input("Enter the new name: ")
                elif edit_choice == "2":
                    updates["description"] = input("Enter the new description: ")
                elif edit_choice == "3":
                    updates["priority"] = input("Enter the new priority: ")
                elif edit_choice == "4":
                    break
                else:
                    print("Please choose a valid option.")

            try:
                tasks = edit_task(tasks, task_id, updates)
                save_tasks(tasks)
                print("Task updated!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            print(f"\n{format_task_list(tasks)}")
            task_id = get_task_id_input("Enter the ID of the task to toggle: ")
            try:
                tasks = toggle_task_complete(tasks, task_id)
                save_tasks(tasks)
                print("Task status toggled!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            print(f"\n{format_task_list(tasks)}")
            task_id = get_task_id_input("Enter the ID of the task to delete: ")

            if get_task_by_id(tasks, task_id) is None:
                print("Task ID not found!")
                continue

            confirm = input(f"Are you sure you want to delete task {task_id}? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("Deletion cancelled.")
                continue

            tasks = delete_task(tasks, task_id)
            save_tasks(tasks)
            print("Task deleted!")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()