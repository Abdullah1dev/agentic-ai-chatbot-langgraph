from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from src.rag import retriever , set_retriever
from langgraph.types import interrupt
from typing import Annotated
from langgraph.prebuilt import InjectedState
from langchain_core.runnables import RunnableConfig
from src.memory import delete_thread
from langchain_core.tools import InjectedToolArg






@tool
def rag_tool(query : str) -> str:
    
    
    """
    Use the uploaded pdf and return relevant information to answer the user question
    Use this tool ONLY when the user is asking questions about the uploaded PDF or document.
    """
    
    print("RAG tool is executed")
    
    
    if retriever  is None:
        return "No document is currently available for retrievel"
    
    
    result = retriever.invoke(query)
    
    context = "\n\n".join(doc.page_content for doc in result)
    
    return context
    
    

@tool
def  delete_conversation(
    config: Annotated[RunnableConfig, InjectedToolArg]
    ) -> str:
    
    
    """
    
    Delete a conversation using its thread ID.
    This tool should only be used when the user explicitly requests to delete a conversation.
    
    """
    
    approval = interrupt(
        "Do you reallly want to Delete this conversation??"
        
    )
    if approval:
           thread_id = config["configurable"]["thread_id"]
           print("Deleting thread:", thread_id)

           delete_thread(thread_id)

           print("Thread deleted")

           return "Conversation deleted Successfully"

    


tools = [rag_tool , delete_conversation]
