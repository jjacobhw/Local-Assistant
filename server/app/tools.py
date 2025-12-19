from langchain.tools import Tool
import os

def list_files(path: str = ".") -> str:
    return "\n".join(os.listdir(path))

list_files_tool = Tool(
    name="list_files",
    func=list_files,
    description="List files in a directory"
)
