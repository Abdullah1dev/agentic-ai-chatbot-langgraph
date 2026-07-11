
from src.state import ChatState
from src.llm import model_with_tools
def chatnode(state : ChatState):
    messages = state["messages"]
    
    response = model_with_tools.invoke(messages)
    
    return {'messages' : [response]}
