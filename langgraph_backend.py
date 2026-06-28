from langgraph.graph import StateGraph , START , END
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage , HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages



load_dotenv()

model = ChatOpenAI(
    model = "openrouter/free",
    api_key =os.getenv("OPEN_AI_API_KEY"),
    base_url =os.getenv("OPENAI_BASE_URL")
     
)



class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages]
    
    

def chatnode(state : ChatState):
    messages = state["messages"]
    
    response = model.invoke(messages)
    
    return {'messages' : [response]}



checkpointer = MemorySaver()

graph = StateGraph(ChatState)

graph.add_node('chatnode' , chatnode)

graph.add_edge(START , 'chatnode')
graph.add_edge('chatnode' , END)

workflow = graph.compile(checkpointer = checkpointer)



