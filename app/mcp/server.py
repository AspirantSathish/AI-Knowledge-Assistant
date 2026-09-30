from mcp.server import MCPServer


mcp = MCPServer("Employee Service")


employees = {
    "EMP001": {
        "name": "John",
        "department": "Engineering",
        "role": "Senior Developer"
    },
    "EMP002": {
        "name": "Priya",
        "department": "Data Science",
        "role": "Data Scientist"
    }
}


leave_balances = {
    "EMP001": {
        "annual_leave": 12,
        "sick_leave": 8
    },
    "EMP002": {
        "annual_leave": 15,
        "sick_leave": 10
    }
}


leave_history = {
    "EMP001": [
        {
            "date": "2026-08-10",
            "days": 2,
            "type": "Annual Leave"
        },
        {
            "date": "2026-09-05",
            "days": 1,
            "type": "Sick Leave"
        }
    ]
}


@mcp.tool()
def get_employee(employee_id: str):
    """Get employee information."""

    employee = employees.get(employee_id)

    if not employee:
        return {"error": "Employee not found"}

    return employee


@mcp.tool()
def get_leave_balance(employee_id: str):
    """Get current leave balance for an employee."""

    balance = leave_balances.get(employee_id)

    if not balance:
        return {"error": "Employee not found"}

    return balance


@mcp.tool()
def get_leave_history(employee_id: str):
    """Get leave history for an employee."""

    history = leave_history.get(employee_id)

    if history is None:
        return {"error": "Employee not found"}

    return history


if __name__ == "__main__":
    mcp.run()