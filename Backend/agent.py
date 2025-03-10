from langgraph.graph import StateGraph
from langchain.tools import Tool
from langchain_mistralai.chat_models import ChatMistral
from langchain_mistralai.embeddings import MistralEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader
import os

# Load API key from environment
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Initialize LLM (Mistral)
llm = ChatMistral(model="mistral-large-latest", api_key=MISTRAL_API_KEY)

# Load and split document
def process_document(file_path: str):
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)
    
    return split_docs

# Initialize retriever using Mistral embeddings
def initialize_retriever(documents):
    embeddings = MistralEmbeddings(api_key=MISTRAL_API_KEY)
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore.as_retriever()

# Define a retrieval tool
def document_retriever(query: str):
    """Retrieve relevant information from the document."""
    return retriever.get_relevant_documents(query)

retrieval_tool = Tool(name="retriever", func=document_retriever, description="Fetches relevant document data.")

# Create RAG agent using LangGraph
def create_rag_agent():
    agent = StateGraph()
    agent.add_node("retrieval", retrieval_tool)
    agent.set_entry_point("retrieval")
    
    return agent.compile()

# Example usage
if __name__ == "__main__":
    file_path = "example.pdf"
    docs = process_document(file_path)
    retriever = initialize_retriever(docs)

    rag_agent = create_rag_agent()
    response = rag_agent.invoke({"query": "What is this document about?"})
    print(response)
