
import pytest

from src.tools.sql_tool import (
    execute_sql_query,
    get_database_schema
)


def test_get_all_employees():
    result = execute_sql_query("""
        SELECT * FROM employees
    """)

    assert result["success"] is True
    assert result["row_count"] == 40


def test_average_salary():
    result = execute_sql_query("""
        SELECT AVG(basic_salary) AS average_salary
        FROM employees
    """)

    assert result["success"] is True
    assert result["rows"][0]["average_salary"] > 0


def test_highest_salary():
    result = execute_sql_query("""
        SELECT first_name, last_name, basic_salary
        FROM employees
        ORDER BY basic_salary DESC
        LIMIT 1
    """)

    assert result["success"] is True
    assert result["row_count"] == 1
    assert result["rows"][0]["basic_salary"] > 0


def test_employee_count_by_department():
    result = execute_sql_query("""
        SELECT d.department_name, COUNT(*) AS total
        FROM employees e
        JOIN departments d
        ON e.department_id = d.department_id
        GROUP BY d.department_name
    """)

    assert result["success"] is True
    assert len(result["rows"]) == 6

    total = sum(row["total"] for row in result["rows"])

    assert total == 40


def test_pending_leave_requests():
    result = execute_sql_query("""
        SELECT *
        FROM leave_requests
        WHERE status = 'Pending'
    """)

    assert result["success"] is True


def test_delete_query_is_rejected():
    result = execute_sql_query("""
        DELETE FROM employees
    """)

    assert result["success"] is False


def test_update_query_is_rejected():
    result = execute_sql_query("""
        UPDATE employees
        SET basic_salary = 0
    """)

    assert result["success"] is False


def test_drop_query_is_rejected():
    result = execute_sql_query("""
        DROP TABLE employees
    """)

    assert result["success"] is False


def test_invalid_sql_is_handled():
    result = execute_sql_query("""
        SELECT unknown_column FROM employees
    """)

    assert result["success"] is False


def test_database_schema():
    schema = get_database_schema()

    assert "employees" in schema
    assert "departments" in schema
    assert "leave_requests" in schema
