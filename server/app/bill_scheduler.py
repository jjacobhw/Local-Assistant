from datetime import date
from bills_config import bills_db
from typing import Dict, List

class BillNotificationService:
    def __init__(self):
        self.notification_days = [7, 3, 1]

    def get_bill_alerts(self) -> Dict[str, List]:
        alerts = {
            "critical": [],
            "urgent": [],
            "upcoming": [],
            "overdue": []
        }

        overdue = bills_db.get_overdue_bills()
        for bill in overdue:
            days_overdue = (date.today() - bill.due_date).days
            alerts["overdue"].append({
                "bill": bill,
                "message": f"OVERDUE: {bill.name} (${bill.amount:.2f}) was due {days_overdue} days ago!",
                "days_overdue": days_overdue
            })

        for days in self.notification_days:
            upcoming = bills_db.get_upcoming_bills(days)
            for bill in upcoming:
                days_until = (bill.due_date - date.today()).days

                if days_until == 0:
                    alerts["critical"].append({
                        "bill": bill,
                        "message": f"DUE TODAY: {bill.name} (${bill.amount:.2f})",
                        "days_until": 0
                    })
                elif days_until == 1:
                    alerts["urgent"].append({
                        "bill": bill,
                        "message": f"Due tomorrow: {bill.name} (${bill.amount:.2f})",
                        "days_until": 1
                    })
                elif days_until <= 7:
                    alerts["upcoming"].append({
                        "bill": bill,
                        "message": f"Due in {days_until} days: {bill.name} (${bill.amount:.2f})",
                        "days_until": days_until
                    })

        return alerts

    def get_notification_summary(self) -> str:
        alerts = self.get_bill_alerts()

        summary = ""

        if alerts["overdue"]:
            summary += "🔴 OVERDUE BILLS:\n"
            for alert in alerts["overdue"]:
                summary += f"  {alert['message']}\n"
            summary += "\n"

        if alerts["critical"]:
            summary += "⚠️ DUE TODAY:\n"
            for alert in alerts["critical"]:
                summary += f"  {alert['message']}\n"
            summary += "\n"

        if alerts["urgent"]:
            summary += "⏰ DUE TOMORROW:\n"
            for alert in alerts["urgent"]:
                summary += f"  {alert['message']}\n"
            summary += "\n"

        if alerts["upcoming"]:
            summary += "📅 UPCOMING (Next 7 days):\n"
            for alert in alerts["upcoming"]:
                summary += f"  {alert['message']}\n"
            summary += "\n"

        if not any(alerts.values()):
            summary = "✅ No upcoming bills in the next 7 days."

        return summary

notification_service = BillNotificationService()
