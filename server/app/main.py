from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent
from langchain_community.chat_models import ChatOllama

app = FastAPI()
llm = ChatOllama(model="gemma3:8b", temperature=0.2)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    response = llm.invoke(req.message)
    return {"response": response.content}