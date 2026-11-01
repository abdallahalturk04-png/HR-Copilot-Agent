
import sqlite3
from pathlib import Path

from config import DATABASE_PATH


MAX_RESULTS = 100

ALLOWED_QUERY_STARTS = ("SELECT", "WITH")


def validate_query(query: str) -> bool:
    """
    Allow read-only SQL queries only.
    """

    if not query or not query.strip():
        raise ValueError("SQL query cannot be empty.")

    normalized_query = query.strip()

    first_word = normalized_query.split()[0].upper()

    if first_word not in ALLOWED_QUERY_STARTS:
        raise ValueError(
            "Only SELECT and WITH queries are allowed."
        )

    return True


def execute_sql_query(query: str) -> dict:
    """
    Execute a read-only SQL query against the HR database.

    Returns query results as a dictionary.
    """

    try:
        validate_query(query)

        database_path = Path(DATABASE_PATH).resolve()

        if not database_path.exists():
            raise FileNotFoundError(
                "HR database was not found."
            )

        # Open database in read-only mode
        database_uri = (
            f"{database_path.as_uri()}?mode=ro"
        )

        connection = sqlite3.connect(
            database_uri,
            uri=True,
            timeout=10
        )

        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            # Execute one SQL statement
            cursor.execute(query)

            columns = [
                description[0]
                for description in cursor.description or []
            ]

            # Fetch one extra row to detect truncation
            fetched_rows = cursor.fetchmany(MAX_RESULTS + 1)

            truncated = len(fetched_rows) > MAX_RESULTS

            fetched_rows = fetched_rows[:MAX_RESULTS]

            rows = [
                dict(row)
                for row in fetched_rows
            ]

            return {
                "success": True,
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
                "truncated": truncated,
                "error": None
            }

        finally:
            connection.close()

    except (sqlite3.Error, ValueError, FileNotFoundError) as error:

        return {
            "success": False,
            "columns": [],
            "rows": [],
            "row_count": 0,
            "truncated": False,
            "error": str(error)
        }


def get_database_schema() -> str:
    """
    Return the database schema to help the AI understand
    available tables and columns.
    """

    schema = {
        "departments": [
            "department_id",
            "department_name"
        ],
        "employees": [
            "employee_id",
            "first_name",
            "last_name",
            "email",
            "department_id",
            "job_title",
            "hire_date",
            "employment_status",
            "basic_salary",
            "allowances",
            "annual_leave_days",
            "used_leave_days"
        ],
        "leave_requests": [
            "request_id",
            "employee_id",
            "start_date",
            "end_date",
            "days_requested",
            "status"
        ]
    }

    description = []

    for table, columns in schema.items():

        description.append(
            f"Table: {table}\n"
            f"Columns: {', '.join(columns)}"
        )

    return "\n\n".join(description)
def get_employee_leave_balance(first_name: str, last_name: str) -> dict:
    """
    Retrieve an employee's annual leave entitlement,
    used leave days, and remaining leave balance.
    """

    database_path = Path(DATABASE_PATH).resolve()

    if not database_path.exists():
        return {
            "success": False,
            "error": "HR database was not found."
        }

    database_uri = f"{database_path.as_uri()}?mode=ro"

    try:
        with sqlite3.connect(
            database_uri,
            uri=True,
            timeout=10
        ) as connection:

            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    first_name,
                    last_name,
                    annual_leave_days,
                    used_leave_days
                FROM employees
                WHERE LOWER(first_name) = LOWER(?)
                  AND LOWER(last_name) = LOWER(?)
            """, (first_name.strip(), last_name.strip()))

            row = cursor.fetchone()

            if row is None:
                return {
                    "success": False,
                    "error": "Employee not found."
                }

            annual = row["annual_leave_days"]
            used = row["used_leave_days"]

            return {
                "success": True,
                "employee_name": f"{row['first_name']} {row['last_name']}",
                "annual_leave_days": annual,
                "used_leave_days": used,
                "remaining_leave_days": annual - used
            }

    except sqlite3.Error as error:
        return {
            "success": False,
            "error": str(error)
        }



if __name__ == "__main__":

    print("HR DATABASE SCHEMA")
    print("==================")

    print(get_database_schema())

    print("\nTESTING SQL QUERY")
    print("=================")

    result = execute_sql_query("""
        SELECT
            department_name,
            COUNT(*) AS employee_count
        FROM employees
        JOIN departments
            ON employees.department_id =
               departments.department_id
        GROUP BY department_name
        ORDER BY employee_count DESC
    """)

    if result["success"]:

        print("\nQuery executed successfully!")

        for row in result["rows"]:
            print(row)

    else:
        print("Query failed:", result["error"])
