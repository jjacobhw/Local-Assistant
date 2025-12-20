from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from datetime import date
from bills_config import bills_db, Bill, BillStatus
from bill_scheduler import notification_service
import uuid

app = FastAPI()

llm = ChatOllama(model="gemma3:8b", temperature=0.2)

class ChatRequest(BaseModel):
    message: str

class BillCreateRequest(BaseModel):
    name: str
    amount: float
    due_date: str
    provider: str
    account_number: str = None

class BillResponse(BaseModel):
    id: str
    name: str
    amount: float
    due_date: date
    status: str
    provider: str
    account_number: str = None

@app.post("/chat")
async def chat(req: ChatRequest):
    response = llm.invoke(req.message)
    return {"response": response.content}

@app.get("/bills")
async def get_all_bills():
    bills = bills_db.get_all_bills()
    return {"bills": [bill.model_dump() for bill in bills]}

@app.post("/bills")
async def create_bill(bill_req: BillCreateRequest):
    try:
        due_date_obj = date.fromisoformat(bill_req.due_date)
        bill = Bill(
            id=str(uuid.uuid4()),
            name=bill_req.name,
            amount=bill_req.amount,
            due_date=due_date_obj,
            status=BillStatus.PENDING,
            provider=bill_req.provider,
            account_number=bill_req.account_number
        )
        bills_db.add_bill(bill)
        return {"message": "Bill created successfully", "bill": bill.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/bills/upcoming")
async def get_upcoming_bills(days: int = 7):
    upcoming = bills_db.get_upcoming_bills(days)
    return {"bills": [bill.model_dump() for bill in upcoming]}

@app.get("/bills/overdue")
async def get_overdue_bills():
    overdue = bills_db.get_overdue_bills()
    return {"bills": [bill.model_dump() for bill in overdue]}

@app.get("/bills/alerts")
async def get_bill_alerts():
    alerts = notification_service.get_bill_alerts()
    summary = notification_service.get_notification_summary()
    return {"alerts": alerts, "summary": summary}

@app.post("/bills/{bill_id}/pay")
async def mark_bill_as_paid(bill_id: str):
    bill = bills_db.mark_as_paid(bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return {"message": f"Bill '{bill.name}' marked as paid", "bill": bill.model_dump()}

@app.delete("/bills/{bill_id}")
async def delete_bill(bill_id: str):
    success = bills_db.delete_bill(bill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bill not found")
    return {"message": "Bill deleted successfully"}
