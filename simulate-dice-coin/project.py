"""
Dice Roller / Coin Flip Simulator (CLI)
Simulates rolls or flips and tracks running statistics like heads/tails counts.

Structure:
- roll_dice / flip_coins: pure random-generation logic
- update_stats / get_stats_summary / format_*_summary / reset_stats: pure, testable
- main: top-level menu loop, all I/O
"""

import random


def roll_dice(num_dice, sides):
    """
    Roll num_dice dice, each with the given number of sides.
    Returns a list of individual results.
    Raises ValueError if num_dice or sides is invalid.
    """
    if num_dice <= 0:
        raise ValueError("Number of dice must be a positive integer")
    if sides < 2:
        raise ValueError("A die must have at least 2 sides")

    return [random.randint(1, sides) for _ in range(num_dice)]


def flip_coins(num_flips):
    """
    Flip a coin num_flips times.
    Returns a list of 'Heads'/'Tails' results.
    Raises ValueError if num_flips is invalid.
    """
    if num_flips <= 0:
        raise ValueError("Number of flips must be a positive integer")

    return [random.choice(["Heads", "Tails"]) for _ in range(num_flips)]


def update_stats(stats, results):
    """
    Update a running-count dict in place given a list of new results.
    Returns the same dict for convenience/chaining.
    """
    for result in results:
        stats[result] = stats.get(result, 0) + 1
    return stats


def get_stats_summary(stats):
    """
    Return (total, breakdown) for a stats dict, where breakdown is a list of
    (key, count, percentage) tuples sorted by key. total is 0 and breakdown
    is [] when stats is empty.
    """
    total = sum(stats.values())
    if total == 0:
        return 0, []

    breakdown = [
        (key, count, (count / total) * 100)
        for key, count in sorted(stats.items(), key=lambda item: str(item[0]))
    ]
    return total, breakdown


def format_dice_summary(stats):
    """Return a formatted multi-line string summarizing dice statistics."""
    total, breakdown = get_stats_summary(stats)
    if total == 0:
        return "No dice rolls yet."

    lines = [f"Total Rolls: {total}", ""]
    for face, count, percentage in breakdown:
        lines.append(f"Side {face}: {count} ({percentage:.1f}%)")
    return "\n".join(lines)


def format_coin_summary(stats):
    """Return a formatted multi-line string summarizing coin flip statistics."""
    total, breakdown = get_stats_summary(stats)
    if total == 0:
        return "No coin flips yet."

    lines = [f"Total Flips: {total}", ""]
    for side, count, percentage in breakdown:
        lines.append(f"{side}: {count} ({percentage:.1f}%)")
    return "\n".join(lines)


def reset_stats(*stats_dicts):
    """Clear every stats dict passed in, in place."""
    for stats in stats_dicts:
        stats.clear()


def get_positive_int(prompt, minimum=1):
    """Repeatedly prompt until the user enters an int >= minimum."""
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"Please enter a number >= {minimum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def main():
    dice_stats = {}
    coin_stats = {}

    while True:
        print(
            "\n===== DICE ROLLER / COIN FLIP SIMULATOR =====\n"
            "1. Roll a Die\n"
            "2. Flip a Coin\n"
            "3. View Statistics\n"
            "4. Reset Statistics\n"
            "5. Exit\n"
            "=============================================="
        )
        choice = input("Enter your choice: ")

        if choice == "1":
            num_dice = get_positive_int("How many dice? ", minimum=1)
            sides = get_positive_int("How many sides per die? ", minimum=2)
            rolls = roll_dice(num_dice, sides)
            print(f"Rolls: {rolls}  Total: {sum(rolls)}")
            update_stats(dice_stats, rolls)

        elif choice == "2":
            num_flips = get_positive_int("How many coins to flip? ", minimum=1)
            flips = flip_coins(num_flips)
            print(f"Results: {flips}")
            update_stats(coin_stats, flips)

        elif choice == "3":
            print("\n--- Dice Statistics ---")
            print(format_dice_summary(dice_stats))
            print("\n--- Coin Statistics ---")
            print(format_coin_summary(coin_stats))

        elif choice == "4":
            confirm = input("Are you sure you want to reset all statistics? (y/n): ").lower()
            if confirm == "y":
                reset_stats(dice_stats, coin_stats)
                print("Statistics have been reset.")
            else:
                print("Reset cancelled.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()