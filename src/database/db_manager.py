
import sqlite3
from config import DATABASE_PATH


def get_connection():
    """
    Create and return a connection to the HR SQLite database.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """
    Create all HR database tables if they do not already exist.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # 1. Departments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                department_id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_name TEXT NOT NULL UNIQUE
            )
        """)

        # 2. Employees table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                department_id INTEGER NOT NULL,
                job_title TEXT NOT NULL,
                hire_date TEXT NOT NULL,
                employment_status TEXT NOT NULL
                    CHECK (employment_status IN (
                        'Active', 'On Leave', 'Resigned'
                    )),
                basic_salary REAL NOT NULL CHECK (basic_salary >= 0),
                allowances REAL NOT NULL DEFAULT 0
                    CHECK (allowances >= 0),
                annual_leave_days INTEGER NOT NULL DEFAULT 21,
                used_leave_days INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (department_id)
                    REFERENCES departments(department_id),
                CHECK (annual_leave_days >= 0),
                CHECK (used_leave_days >= 0)
            )
        """)

        # 3. Leave requests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leave_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                days_requested INTEGER NOT NULL
                    CHECK (days_requested > 0),
                status TEXT NOT NULL
                    CHECK (status IN (
                        'Pending', 'Approved', 'Rejected'
                    )),
                FOREIGN KEY (employee_id)
                    REFERENCES employees(employee_id),
                CHECK (end_date >= start_date)
            )
        """)

        # Indexes to improve query performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_employees_department
            ON employees(department_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_leave_employee
            ON leave_requests(employee_id)
        """)

        connection.commit()

        print("HR database initialized successfully!")
        print("Tables created: departments, employees, leave_requests")

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
