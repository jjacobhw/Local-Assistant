from langchain.agents import initialize_agent, AgentType
from tools import (
    list_files_tool,
    check_upcoming_bills_tool,
    check_overdue_bills_tool,
    add_bill_tool,
    mark_paid_tool,
    list_bills_tool
)
from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma3:8b", temperature=0.2)

agent = initialize_agent(
    tools=[
        list_files_tool,
        check_upcoming_bills_tool,
        check_overdue_bills_tool,
        add_bill_tool,
        mark_paid_tool,
        list_bills_tool
    ],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

def run_agent(message: str) -> str:
    return agent.run(message)
