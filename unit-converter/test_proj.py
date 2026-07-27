import pytest
from Unit_Converter import convert_temperature, convert_length, convert_weight


def test_convert_temperature():
    assert convert_temperature(0, "C", "F") == pytest.approx(32)
    assert convert_temperature(100, "C", "F") == pytest.approx(212)
    assert convert_temperature(32, "F", "C") == pytest.approx(0)
    assert convert_temperature(0, "C", "K") == pytest.approx(273.15)
    assert convert_temperature(273.15, "K", "C") == pytest.approx(0)

    # Below absolute zero should raise
    with pytest.raises(ValueError):
        convert_temperature(-300, "C", "F")
    with pytest.raises(ValueError):
        convert_temperature(-10, "K", "C")

    # Unsupported unit should raise
    with pytest.raises(ValueError):
        convert_temperature(100, "C", "X")


def test_convert_length():
    assert convert_length(1, "km", "m") == pytest.approx(1000)
    assert convert_length(100, "cm", "m") == pytest.approx(1)
    assert convert_length(1, "in", "cm") == pytest.approx(2.54)
    assert convert_length(1, "mi", "km") == pytest.approx(1.609344)
    assert convert_length(0, "m", "km") == pytest.approx(0)

    # Negative length should raise
    with pytest.raises(ValueError):
        convert_length(-5, "m", "km")

    # Unsupported unit should raise
    with pytest.raises(ValueError):
        convert_length(5, "m", "furlong")


def test_convert_weight():
    assert convert_weight(1, "kg", "g") == pytest.approx(1000)
    assert convert_weight(1000, "g", "kg") == pytest.approx(1)
    assert convert_weight(1, "kg", "lb") == pytest.approx(2.20462, rel=1e-4)
    assert convert_weight(16, "oz", "lb") == pytest.approx(1, rel=1e-3)

    # Negative weight should raise
    with pytest.raises(ValueError):
        convert_weight(-1, "kg", "g")

    # Unsupported unit should raise
    with pytest.raises(ValueError):
        convert_weight(1, "kg", "stone")