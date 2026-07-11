from langgraph.graph import StateGraph, START
from src.memory import checkpointer, retrieve_all_threads
from src.state import ChatState
from src.rag import initialize_rag, set_retriever
from src.tools import tools
from src.nodes import chatnode

from langgraph.prebuilt import ToolNode, tools_condition
    




tool_node = ToolNode(tools)

graph = StateGraph(ChatState)

graph.add_node('chatnode' , chatnode)
graph.add_node('tools' , tool_node)

graph.add_edge(START , 'chatnode')
graph.add_conditional_edges("chatnode" , tools_condition)
graph.add_edge("tools", "chatnode")

workflow = graph.compile(checkpointer = checkpointer)



