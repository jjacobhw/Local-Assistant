from langchain.tools import Tool
import os
from datetime import date
from bills_config import bills_db, Bill, BillStatus
import uuid

def list_files(path: str = ".") -> str:
    return "\n".join(os.listdir(path))

def check_upcoming_bills(days_ahead: int = 7) -> str:
    upcoming = bills_db.get_upcoming_bills(days_ahead)
    if not upcoming:
        return f"No bills due in the next {days_ahead} days."

    result = f"Upcoming bills in the next {days_ahead} days:\n\n"
    for bill in upcoming:
        days_until = (bill.due_date - date.today()).days
        result += f"- {bill.name}: ${bill.amount:.2f} due on {bill.due_date} ({days_until} days)\n"
        result += f"  Provider: {bill.provider}, Status: {bill.status}\n\n"
    return result

def check_overdue_bills() -> str:
    overdue = bills_db.get_overdue_bills()
    if not overdue:
        return "No overdue bills."

    result = "OVERDUE BILLS:\n\n"
    for bill in overdue:
        days_overdue = (date.today() - bill.due_date).days
        result += f"- {bill.name}: ${bill.amount:.2f} was due on {bill.due_date} ({days_overdue} days overdue)\n"
        result += f"  Provider: {bill.provider}\n\n"
    return result

def add_new_bill(name: str, amount: float, due_date: str, provider: str, account_number: str = "") -> str:
    try:
        due_date_obj = date.fromisoformat(due_date)
        bill = Bill(
            id=str(uuid.uuid4()),
            name=name,
            amount=amount,
            due_date=due_date_obj,
            status=BillStatus.PENDING,
            provider=provider,
            account_number=account_number if account_number else None
        )
        bills_db.add_bill(bill)
        return f"Successfully added bill: {name} for ${amount:.2f} due on {due_date}"
    except Exception as e:
        return f"Error adding bill: {str(e)}"

def mark_bill_paid(bill_name: str) -> str:
    bills = bills_db.get_all_bills()
    matching_bills = [b for b in bills if bill_name.lower() in b.name.lower() and b.status != BillStatus.PAID]

    if not matching_bills:
        return f"No pending bill found matching '{bill_name}'"

    if len(matching_bills) > 1:
        result = f"Multiple bills found matching '{bill_name}':\n"
        for bill in matching_bills:
            result += f"- {bill.name} (${bill.amount:.2f}, due {bill.due_date})\n"
        return result + "\nPlease be more specific."

    bill = matching_bills[0]
    bills_db.mark_as_paid(bill.id)
    return f"Marked '{bill.name}' as paid (${bill.amount:.2f})"

def list_all_bills() -> str:
    bills = bills_db.get_all_bills()
    if not bills:
        return "No bills in the system."

    result = "All bills:\n\n"
    for bill in bills:
        result += f"- {bill.name}: ${bill.amount:.2f} due on {bill.due_date}\n"
        result += f"  Status: {bill.status}, Provider: {bill.provider}\n\n"
    return result

list_files_tool = Tool(
    name="list_files",
    func=list_files,
    description="List files in a directory"
)

check_upcoming_bills_tool = Tool(
    name="check_upcoming_bills",
    func=check_upcoming_bills,
    description="Check bills due in the next N days (default 7). Input should be number of days ahead to check."
)

check_overdue_bills_tool = Tool(
    name="check_overdue_bills",
    func=check_overdue_bills,
    description="Check for overdue bills that need immediate attention"
)

add_bill_tool = Tool(
    name="add_bill",
    func=add_new_bill,
    description="Add a new bill. Input format: 'name,amount,due_date(YYYY-MM-DD),provider,account_number'"
)

mark_paid_tool = Tool(
    name="mark_bill_paid",
    func=mark_bill_paid,
    description="Mark a bill as paid. Input should be the bill name."
)

list_bills_tool = Tool(
    name="list_all_bills",
    func=list_all_bills,
    description="List all bills in the system with their status"
)
