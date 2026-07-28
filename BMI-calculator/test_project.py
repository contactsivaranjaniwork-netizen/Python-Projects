import pytest
from project import (
    calculate_bmi,
    classify_bmi,
    calculate_bmr,
    calculate_daily_calories,
)


def test_calculate_bmi():
    # 70kg, 175cm -> 70 / 1.75^2 = 22.857...
    assert calculate_bmi(70, 175) == pytest.approx(22.857, rel=1e-3)
    assert calculate_bmi(50, 160) == pytest.approx(19.531, rel=1e-3)

    with pytest.raises(ValueError):
        calculate_bmi(0, 175)
    with pytest.raises(ValueError):
        calculate_bmi(70, 0)
    with pytest.raises(ValueError):
        calculate_bmi(-70, 175)


def test_classify_bmi_boundaries():
    assert classify_bmi(18.4) == "Underweight"
    assert classify_bmi(18.5) == "Normal weight"   # boundary now included correctly
    assert classify_bmi(24.9) == "Normal weight"
    assert classify_bmi(25) == "Overweight"        # boundary now included correctly
    assert classify_bmi(29.9) == "Overweight"
    assert classify_bmi(30) == "Obese"             # boundary now included correctly
    assert classify_bmi(35) == "Obese"

    with pytest.raises(ValueError):
        classify_bmi(0)
    with pytest.raises(ValueError):
        classify_bmi(-5)


def test_calculate_bmr():
    # Men: 10*70 + 6.25*175 - 5*30 + 5 = 700 + 1093.75 - 150 + 5 = 1648.75
    assert calculate_bmr(70, 175, 30, "M") == pytest.approx(1648.75)
    assert calculate_bmr(70, 175, 30, "m") == pytest.approx(1648.75)

    # Women: 10*60 + 6.25*165 - 5*25 - 161 = 600 + 1031.25 - 125 - 161 = 1345.25
    assert calculate_bmr(60, 165, 25, "F") == pytest.approx(1345.25)

    with pytest.raises(ValueError):
        calculate_bmr(70, 175, 30, "X")
    with pytest.raises(ValueError):
        calculate_bmr(0, 175, 30, "M")
    with pytest.raises(ValueError):
        calculate_bmr(70, 175, -5, "M")


def test_calculate_daily_calories():
    bmr = 1600
    assert calculate_daily_calories(bmr, "1") == pytest.approx(1920)   # 1600 * 1.2
    assert calculate_daily_calories(bmr, "2") == pytest.approx(2200)   # 1600 * 1.375
    assert calculate_daily_calories(bmr, "3") == pytest.approx(2480)   # 1600 * 1.55
    assert calculate_daily_calories(bmr, "4") == pytest.approx(2760)   # 1600 * 1.725

    with pytest.raises(ValueError):
        calculate_daily_calories(bmr, "5")
    with pytest.raises(ValueError):
        calculate_daily_calories(bmr, "sedentary")