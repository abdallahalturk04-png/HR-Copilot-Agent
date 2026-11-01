
from datetime import date


def calculate_remaining_leave(
    annual_leave_days: float,
    used_leave_days: float
) -> dict:
    """Calculate remaining annual leave balance."""

    if annual_leave_days < 0 or used_leave_days < 0:
        raise ValueError("Leave days cannot be negative.")

    if used_leave_days > annual_leave_days:
        raise ValueError("Used leave cannot exceed annual leave.")

    remaining = annual_leave_days - used_leave_days

    return {
        "calculation": "remaining_leave",
        "annual_leave_days": annual_leave_days,
        "used_leave_days": used_leave_days,
        "remaining_leave_days": remaining
    }


def calculate_monthly_salary(
    basic_salary: float,
    allowances: float
) -> dict:
    """Calculate total monthly salary."""

    if basic_salary < 0 or allowances < 0:
        raise ValueError("Salary values cannot be negative.")

    total = basic_salary + allowances

    return {
        "calculation": "monthly_salary",
        "basic_salary": basic_salary,
        "allowances": allowances,
        "total_monthly_salary": round(total, 2)
    }


def calculate_end_of_service(
    basic_salary: float,
    hire_date: str,
    end_date: str | None = None
) -> dict:
    """
    Estimate end-of-service gratuity using a configurable
    illustrative formula.

    Formula:
    21 days of basic salary per service year.

    This is NOT a legal calculation.
    """

    if basic_salary < 0:
        raise ValueError("Salary cannot be negative.")

    start = date.fromisoformat(hire_date)

    end = (
        date.fromisoformat(end_date)
        if end_date
        else date.today()
    )

    if end < start:
        raise ValueError("End date cannot precede hire date.")

    service_days = (end - start).days

    service_years = service_days / 365.25

    daily_salary = basic_salary / 30

    gratuity = (
        daily_salary * 21 * service_years
    )

    return {
        "calculation": "end_of_service",
        "basic_salary": basic_salary,
        "service_days": service_days,
        "service_years": round(service_years, 2),
        "estimated_gratuity": round(gratuity, 2),
        "formula": "21 days of basic salary per service year",
        "legal_notice": "Illustrative estimate only. Actual entitlement depends on applicable law and company policy."
    }


if __name__ == "__main__":

    print("TEST 1: Remaining Leave")

    print(
        calculate_remaining_leave(21, 5)
    )

    print("\nTEST 2: Monthly Salary")

    print(
        calculate_monthly_salary(1000, 150)
    )

    print("\nTEST 3: End of Service")

    print(
        calculate_end_of_service(
            1000,
            "2022-01-01"
        )
    )
