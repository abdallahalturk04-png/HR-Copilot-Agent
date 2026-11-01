
import pytest

from src.tools.calculator_tool import (
    calculate_remaining_leave,
    calculate_monthly_salary,
    calculate_end_of_service
)


def test_remaining_leave():
    result = calculate_remaining_leave(21, 5)

    assert result["remaining_leave_days"] == 16


def test_zero_used_leave():
    result = calculate_remaining_leave(21, 0)

    assert result["remaining_leave_days"] == 21


def test_invalid_leave_balance():
    with pytest.raises(ValueError):
        calculate_remaining_leave(21, 25)


def test_negative_leave():
    with pytest.raises(ValueError):
        calculate_remaining_leave(-5, 2)


def test_monthly_salary():
    result = calculate_monthly_salary(1000, 150)

    assert result["total_monthly_salary"] == 1150


def test_zero_allowances():
    result = calculate_monthly_salary(1000, 0)

    assert result["total_monthly_salary"] == 1000


def test_negative_salary():
    with pytest.raises(ValueError):
        calculate_monthly_salary(-1000, 150)


def test_end_of_service():
    result = calculate_end_of_service(
        1000,
        "2022-01-01",
        "2023-01-01"
    )

    assert result["estimated_gratuity"] > 0
    assert result["service_years"] > 0


def test_invalid_hire_date():
    with pytest.raises(ValueError):
        calculate_end_of_service(
            1000,
            "2025-01-01",
            "2024-01-01"
        )


def test_negative_basic_salary():
    with pytest.raises(ValueError):
        calculate_end_of_service(
            -1000,
            "2022-01-01"
        )
