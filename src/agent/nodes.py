import json

from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from config import OLLAMA_MODEL, OLLAMA_BASE_URL

from src.agent.state import AgentState
from src.agent.prompts import HR_SYSTEM_PROMPT

from src.tools.policy_tool import search_hr_policies

from src.tools.sql_tool import (
    execute_sql_query,
    get_database_schema,
    get_employee_leave_balance
)

from src.tools.calculator_tool import (
    calculate_remaining_leave,
    calculate_monthly_salary,
    calculate_end_of_service
)


# --------------------------------------------------
# SQL TOOLS
# --------------------------------------------------

@tool
def get_hr_database_schema() -> str:
    """Get the available HR database tables and columns."""
    return get_database_schema()


@tool
def query_hr_database(query: str) -> str:
    """Execute a read-only SELECT or WITH SQL query."""
    result = execute_sql_query(query)

    return json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    )


# --------------------------------------------------
# EMPLOYEE LEAVE TOOL
# --------------------------------------------------

@tool
def employee_leave_balance_tool(
    first_name: str,
    last_name: str
) -> str:
    """
    Get an employee's annual leave entitlement,
    used leave days, and remaining leave balance.
    """

    result = get_employee_leave_balance(
        first_name,
        last_name
    )

    return json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    )


# --------------------------------------------------
# CALCULATOR TOOLS
# --------------------------------------------------

@tool
def remaining_leave_calculator(
    annual_leave_days: float,
    used_leave_days: float
) -> str:
    """Calculate an employee's remaining annual leave balance."""

    result = calculate_remaining_leave(
        annual_leave_days,
        used_leave_days
    )

    return json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    )


@tool
def monthly_salary_calculator(
    basic_salary: float,
    allowances: float
) -> str:
    """Calculate total monthly salary from basic salary and allowances."""

    result = calculate_monthly_salary(
        basic_salary,
        allowances
    )

    return json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    )


@tool
def end_of_service_calculator(
    basic_salary: float,
    hire_date: str,
    end_date: str = ""
) -> str:
    """Calculate an illustrative end-of-service estimate.
    This is not a legal calculation.
    """

    result = calculate_end_of_service(
        basic_salary,
        hire_date,
        end_date if end_date else None
    )

    return json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    )


# --------------------------------------------------
# AVAILABLE HR TOOLS
# --------------------------------------------------

HR_TOOLS = [
    search_hr_policies,
    get_hr_database_schema,
    query_hr_database,
    employee_leave_balance_tool,
    remaining_leave_calculator,
    monthly_salary_calculator,
    end_of_service_calculator
]


# --------------------------------------------------
# OLLAMA MODEL
# --------------------------------------------------

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0
)

llm_with_tools = llm.bind_tools(HR_TOOLS)


# --------------------------------------------------
# AGENT NODE
# --------------------------------------------------

def agent_node(state: AgentState) -> dict:
    """
    Process the conversation and decide whether
    to answer directly or call an HR tool.
    """

    conversation = [
        SystemMessage(content=HR_SYSTEM_PROMPT)
    ]

    conversation.extend(
        state.get("messages", [])
    )

    response = llm_with_tools.invoke(conversation)

    return {
        "messages": [response]
    }