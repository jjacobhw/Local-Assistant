from langchain.agents import initialize_agent, AgentType
from tools import list_files_tool
from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma3:8b", temperature=0.2)

agent = initialize_agent(
    tools=[list_files_tool],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

def run_agent(message: str) -> str:
    return agent.run(message)
