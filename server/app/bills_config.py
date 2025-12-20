from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
from enum import Enum
import json
import os

class BillStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"

class Bill(BaseModel):
    id: str
    name: str
    amount: float
    due_date: date
    status: BillStatus
    auto_pay_enabled: bool = False
    provider: str
    account_number: Optional[str] = None
    last_paid_date: Optional[date] = None

class BillsDatabase:
    def __init__(self, db_path: str = "bills_db.json"):
        self.db_path = db_path
        self.bills: List[Bill] = []
        self.load_bills()

    def load_bills(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                data = json.load(f)
                self.bills = [Bill(**bill) for bill in data]
        else:
            self.bills = []

    def save_bills(self):
        with open(self.db_path, 'w') as f:
            json.dump([bill.model_dump(mode='json') for bill in self.bills], f, indent=2, default=str)

    def add_bill(self, bill: Bill) -> Bill:
        self.bills.append(bill)
        self.save_bills()
        return bill

    def get_bill(self, bill_id: str) -> Optional[Bill]:
        for bill in self.bills:
            if bill.id == bill_id:
                return bill
        return None

    def update_bill(self, bill_id: str, updated_bill: Bill) -> Optional[Bill]:
        for i, bill in enumerate(self.bills):
            if bill.id == bill_id:
                self.bills[i] = updated_bill
                self.save_bills()
                return updated_bill
        return None

    def delete_bill(self, bill_id: str) -> bool:
        for i, bill in enumerate(self.bills):
            if bill.id == bill_id:
                del self.bills[i]
                self.save_bills()
                return True
        return False

    def get_all_bills(self) -> List[Bill]:
        return self.bills

    def get_upcoming_bills(self, days_ahead: int = 7) -> List[Bill]:
        today = date.today()
        upcoming = []
        for bill in self.bills:
            if bill.status == BillStatus.PENDING:
                days_until_due = (bill.due_date - today).days
                if 0 <= days_until_due <= days_ahead:
                    upcoming.append(bill)
        return sorted(upcoming, key=lambda x: x.due_date)

    def get_overdue_bills(self) -> List[Bill]:
        today = date.today()
        overdue = []
        for bill in self.bills:
            if bill.due_date < today and bill.status == BillStatus.PENDING:
                bill.status = BillStatus.OVERDUE
                overdue.append(bill)
        if overdue:
            self.save_bills()
        return overdue

    def mark_as_paid(self, bill_id: str) -> Optional[Bill]:
        bill = self.get_bill(bill_id)
        if bill:
            bill.status = BillStatus.PAID
            bill.last_paid_date = date.today()
            self.save_bills()
            return bill
        return None

bills_db = BillsDatabase()
