from langgraph.graph import StateGraph , START , END
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage , HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS






load_dotenv()

model = ChatOpenAI(
    model = "openrouter/free",
    api_key =os.getenv("OPEN_AI_API_KEY"),
    base_url =os.getenv("OPENAI_BASE_URL")
     
)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

def initialize_rag(uploaded_file):
    os.makedirs("temp/" , exist_ok=True)
    
    try:
        
        pdf_path = os.path.join("temp/" , uploaded_file.name)
         
        with open(pdf_path , 'wb') as f:
            f.write(uploaded_file.getvalue())
            
        
        loader = PyPDFLoader(pdf_path)
        
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100
        )
        
        chunks = text_splitter.split_documents(documents)
        
        vector_store = FAISS.from_documents(chunks , embeddings)
        
        retriever = vector_store.as_retriever(
        search_type = 'similarity',
        search_kwargs = {"k" : 4}
        
        )
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            
        
        
        return retriever 
    
    except Exception as e:
        raise e
    
    


    


class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages]
    
    

def chatnode(state : ChatState):
    messages = state["messages"]
    
    response = model.invoke(messages)
    
    return {'messages' : [response]}


conn = sqlite3.connect('chatbot.db' , check_same_thread=False)

checkpointer = SqliteSaver(conn = conn)


graph = StateGraph(ChatState)

graph.add_node('chatnode' , chatnode)

graph.add_edge(START , 'chatnode')
graph.add_edge('chatnode' , END)

workflow = graph.compile(checkpointer = checkpointer)
print("Graph Compiled")


def retrieve_all_threads():
    print("Function Defined")
    
    all_threads = set()
    
    
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    
    return list(all_threads)
