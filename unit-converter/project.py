def convert_temperature(value, from_unit, to_unit):
    """
    Convert a temperature value between Celsius (C), Fahrenheit (F), and Kelvin (K).
    Raises ValueError for unsupported units or physically impossible temperatures.
    """
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    valid_units = ("C", "F", "K")

    if from_unit not in valid_units or to_unit not in valid_units:
        raise ValueError("Unsupported temperature unit")

    # Reject values below absolute zero before converting
    if from_unit == "C" and value < -273.15:
        raise ValueError("Temperature below absolute zero")
    if from_unit == "F" and value < -459.67:
        raise ValueError("Temperature below absolute zero")
    if from_unit == "K" and value < 0:
        raise ValueError("Temperature below absolute zero")

    # Normalize to Celsius first, then convert to target
    if from_unit == "C":
        celsius = value
    elif from_unit == "F":
        celsius = (value - 32) * 5 / 9
    else:  # K
        celsius = value - 273.15

    if to_unit == "C":
        return celsius
    elif to_unit == "F":
        return (celsius * 9 / 5) + 32
    else:  # K
        return celsius + 273.15


def convert_length(value, from_unit, to_unit):
    """
    Convert a length value between m, km, cm, mm, mi, ft, and in.
    Raises ValueError for unsupported units or negative lengths.
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # All factors convert FROM the unit TO meters
    to_meters = {
        "m": 1,
        "km": 1000,
        "cm": 0.01,
        "mm": 0.001,
        "mi": 1609.344,
        "ft": 0.3048,
        "in": 0.0254,
    }

    if from_unit not in to_meters or to_unit not in to_meters:
        raise ValueError("Unsupported length unit")
    if value < 0:
        raise ValueError("Length cannot be negative")

    meters = value * to_meters[from_unit]
    return meters / to_meters[to_unit]


def convert_weight(value, from_unit, to_unit):
    """
    Convert a weight value between kg, g, lb, and oz.
    Raises ValueError for unsupported units or negative weights.
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # All factors convert FROM the unit TO grams
    to_grams = {
        "kg": 1000,
        "g": 1,
        "lb": 453.592,
        "oz": 28.3495,
    }

    if from_unit not in to_grams or to_unit not in to_grams:
        raise ValueError("Unsupported weight unit")
    if value < 0:
        raise ValueError("Weight cannot be negative")

    grams = value * to_grams[from_unit]
    return grams / to_grams[to_unit]


def get_float(prompt):
    """Repeatedly prompt until the user enters a valid float."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid numeric value.")


def temperature_menu():
    options = {
        "1": ("C", "F"),
        "2": ("F", "C"),
        "3": ("C", "K"),
        "4": ("K", "C"),
        "5": ("F", "K"),
        "6": ("K", "F"),
    }
    while True:
        choice = input(
            "=====  Temperature Conversion  =====\n"
            " 1. Celsius to Fahrenheit\n"
            " 2. Fahrenheit to Celsius\n"
            " 3. Celsius to Kelvin\n"
            " 4. Kelvin to Celsius\n"
            " 5. Fahrenheit to Kelvin\n"
            " 6. Kelvin to Fahrenheit\n"
            "======================\n"
            "Choice: "
        )
        if choice not in options:
            print("Invalid choice")
            continue
        from_unit, to_unit = options[choice]
        value = get_float(f"Enter temp in {from_unit}: ")
        try:
            result = convert_temperature(value, from_unit, to_unit)
            print(f"{value:.2f} °{from_unit} = {result:.2f} °{to_unit}")
        except ValueError as e:
            print(f"Error: {e}")
        break


def length_menu():
    options = {
        "1": ("m", "km"),
        "2": ("km", "m"),
        "3": ("m", "cm"),
        "4": ("cm", "m"),
        "5": ("in", "cm"),
        "6": ("cm", "in"),
        "7": ("mi", "km"),
        "8": ("ft", "m"),
    }
    while True:
        choice = input(
            "===== Length Conversion =====\n"
            " 1. Meters to Kilometers\n"
            " 2. Kilometers to Meters\n"
            " 3. Meters to Centimeters\n"
            " 4. Centimeters to Meters\n"
            " 5. Inches to Centimeters\n"
            " 6. Centimeters to Inches\n"
            " 7. Miles to Kilometers\n"
            " 8. Feet to Meters\n"
            "======================\n"
            "Choice: "
        )
        if choice not in options:
            print("Invalid choice")
            continue
        from_unit, to_unit = options[choice]
        value = get_float(f"Enter length in {from_unit}: ")
        try:
            result = convert_length(value, from_unit, to_unit)
            print(f"{value:.2f} {from_unit} = {result:.2f} {to_unit}")
        except ValueError as e:
            print(f"Error: {e}")
        break


def weight_menu():
    options = {
        "1": ("kg", "g"),
        "2": ("g", "kg"),
        "3": ("kg", "lb"),
        "4": ("lb", "kg"),
        "5": ("lb", "oz"),
        "6": ("oz", "lb"),
    }
    while True:
        choice = input(
            "===== Weight Conversion =====\n"
            " 1. Kilograms to Grams\n"
            " 2. Grams to Kilograms\n"
            " 3. Kilograms to Pounds\n"
            " 4. Pounds to Kilograms\n"
            " 5. Pounds to Ounces\n"
            " 6. Ounces to Pounds\n"
            "======================\n"
            "Choice: "
        )
        if choice not in options:
            print("Invalid choice")
            continue
        from_unit, to_unit = options[choice]
        value = get_float(f"Enter weight in {from_unit}: ")
        try:
            result = convert_weight(value, from_unit, to_unit)
            print(f"{value:.2f} {from_unit} = {result:.2f} {to_unit}")
        except ValueError as e:
            print(f"Error: {e}")
        break


def main():
    while True:
        choice = input(
            "=====  UNIT CONVERTER =====\n"
            " 1. Temperature Conversion\n"
            " 2. Length Conversion\n"
            " 3. Weight Conversion\n"
            "======================\n"
            "Enter your choice: "
        )
        if choice == "1":
            temperature_menu()
        elif choice == "2":
            length_menu()
        elif choice == "3":
            weight_menu()
        else:
            print("Invalid choice")

        again = input("Do you want another conversion? (y/n): ").lower()
        if again != "y":
            print("Thank you for using the Converter!")
            break


if __name__ == "__main__":
    main()