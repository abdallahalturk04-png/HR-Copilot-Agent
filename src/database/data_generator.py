
import random
from datetime import date, timedelta

from src.database.db_manager import (
    get_connection,
    initialize_database
)


# Reproducible synthetic data
random.seed(42)


DEPARTMENTS = [
    "Human Resources",
    "Engineering",
    "Finance",
    "Marketing",
    "Sales",
    "IT Support"
]


FIRST_NAMES = [
    "Ahmad", "Omar", "Khaled", "Yousef", "Ali",
    "Sara", "Lina", "Noor", "Maya", "Dana",
    "Adam", "Zaid", "Tareq", "Rami", "Sami",
    "Leen", "Hana", "Salma", "Yara", "Farah"
]


LAST_NAMES = [
    "Hassan", "Khalil", "Nasser", "Saleh", "Othman",
    "Mahmoud", "Ibrahim", "Awad", "Hamdan", "Karim",
    "Mansour", "Qasem", "Abdullah", "Saeed", "Faris"
]


JOB_TITLES = {
    "Human Resources": [
        "HR Manager", "HR Specialist",
        "Recruiter", "HR Coordinator"
    ],
    "Engineering": [
        "Software Engineer", "Data Engineer",
        "Backend Developer", "ML Engineer"
    ],
    "Finance": [
        "Accountant", "Financial Analyst",
        "Finance Manager"
    ],
    "Marketing": [
        "Marketing Specialist", "Content Creator",
        "Digital Marketing Manager"
    ],
    "Sales": [
        "Sales Representative", "Sales Manager",
        "Account Executive"
    ],
    "IT Support": [
        "IT Specialist", "System Administrator",
        "Technical Support Engineer"
    ]
}


def random_date(start_date, end_date):
    """Generate a random date within a given range."""

    days_difference = (end_date - start_date).days

    random_days = random.randint(0, days_difference)

    return start_date + timedelta(days=random_days)


def generate_employees(department_ids):
    """Generate 40 synthetic employee records."""

    today = date.today()

    used_names = set()
    employees = []

    for number in range(1, 41):

        # Generate unique employee names
        while True:
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)

            full_name = (first_name, last_name)

            if full_name not in used_names:
                used_names.add(full_name)
                break

        employee_id = f"EMP{number:03d}"

        email = (
            f"{first_name.lower()}."
            f"{last_name.lower()}{number}@company.com"
        )

        department = random.choice(DEPARTMENTS)

        department_id = department_ids[department]

        job_title = random.choice(JOB_TITLES[department])

        hire_date = random_date(
            date(2019, 1, 1),
            today - timedelta(days=90)
        )

        employment_status = random.choices(
            ["Active", "On Leave", "Resigned"],
            weights=[85, 10, 5]
        )[0]

        basic_salary = round(
            random.uniform(450, 1800), 2
        )

        allowances = round(
            random.uniform(30, 250), 2
        )

        annual_leave_days = random.choice(
            [14, 18, 21, 24, 30]
        )

        employees.append({
            "employee_id": employee_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "department_id": department_id,
            "job_title": job_title,
            "hire_date": hire_date.isoformat(),
            "employment_status": employment_status,
            "basic_salary": basic_salary,
            "allowances": allowances,
            "annual_leave_days": annual_leave_days,
            "used_leave_days": 0
        })

    return employees


def generate_leave_requests(cursor, employees):
    """Generate synthetic employee leave requests."""

    today = date.today()

    requests = []

    for employee in employees:

        employee_id = employee["employee_id"]

        annual_leave = employee["annual_leave_days"]

        remaining_approved_days = annual_leave

        number_of_requests = random.randint(1, 3)

        used_leave_days = 0

        for _ in range(number_of_requests):

            status = random.choices(
                ["Approved", "Pending", "Rejected"],
                weights=[60, 25, 15]
            )[0]

            if status == "Approved":

                max_days = min(
                    7,
                    remaining_approved_days
                )

                if max_days < 1:
                    continue

                days_requested = random.randint(
                    1,
                    max_days
                )

                remaining_approved_days -= days_requested

                used_leave_days += days_requested

            else:
                days_requested = random.randint(1, 7)

            start_date = random_date(
                today - timedelta(days=365),
                today
            )

            end_date = start_date + timedelta(
                days=days_requested - 1
            )

            requests.append((
                employee_id,
                start_date.isoformat(),
                end_date.isoformat(),
                days_requested,
                status
            ))

        employee["used_leave_days"] = used_leave_days

    cursor.executemany("""
        INSERT INTO leave_requests (
            employee_id,
            start_date,
            end_date,
            days_requested,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, requests)


def populate_database():
    """Populate the HR database with synthetic data."""

    initialize_database()

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Prevent duplicate employee records
        existing_count = cursor.execute("""
            SELECT COUNT(*)
            FROM employees
        """).fetchone()[0]

        if existing_count > 0:

            print(
                f"Database already contains "
                f"{existing_count} employees."
            )

            print("No new data was inserted.")

            return

        # Insert departments
        cursor.executemany("""
            INSERT OR IGNORE INTO departments (
                department_name
            )
            VALUES (?)
        """, [(name,) for name in DEPARTMENTS])

        # Retrieve department IDs
        rows = cursor.execute("""
            SELECT department_id, department_name
            FROM departments
        """).fetchall()

        department_ids = {
            row["department_name"]: row["department_id"]
            for row in rows
        }

        # Generate employee records
        employees = generate_employees(department_ids)

        # Insert employees
        cursor.executemany("""
            INSERT INTO employees (
                employee_id,
                first_name,
                last_name,
                email,
                department_id,
                job_title,
                hire_date,
                employment_status,
                basic_salary,
                allowances,
                annual_leave_days,
                used_leave_days
            )
            VALUES (
                :employee_id,
                :first_name,
                :last_name,
                :email,
                :department_id,
                :job_title,
                :hire_date,
                :employment_status,
                :basic_salary,
                :allowances,
                :annual_leave_days,
                :used_leave_days
            )
        """, employees)

        # Generate leave requests
        generate_leave_requests(cursor, employees)

        # Update employees with approved leave days
        cursor.executemany("""
            UPDATE employees
            SET used_leave_days = :used_leave_days
            WHERE employee_id = :employee_id
        """, employees)

        connection.commit()

        # Display database summary
        employee_count = cursor.execute("""
            SELECT COUNT(*)
            FROM employees
        """).fetchone()[0]

        department_count = cursor.execute("""
            SELECT COUNT(*)
            FROM departments
        """).fetchone()[0]

        leave_count = cursor.execute("""
            SELECT COUNT(*)
            FROM leave_requests
        """).fetchone()[0]

        print("\nHR DATABASE POPULATED SUCCESSFULLY!")
        print("-----------------------------------")
        print("Employees:", employee_count)
        print("Departments:", department_count)
        print("Leave Requests:", leave_count)

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    populate_database()
