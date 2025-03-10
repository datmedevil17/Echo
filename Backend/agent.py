from langgraph.graph import StateGraph
from langgraph.prebuilt import create_llm_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType
from langchain.tools import Tool
from retriever import retrieve_documents

# Load Mistral API Key from .env
import os
from dotenv import load_dotenv

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Define LLM with Mistral
llm = ChatOpenAI(model="mistral-large-latest", openai_api_key=MISTRAL_API_KEY)

# Define document retrieval tool
def search_docs(query: str):
    return retrieve_documents(query)  # Calls the retriever

retrieval_tool = Tool(
    name="DocumentRetriever",
    func=search_docs,
    description="Retrieves relevant documents based on the query.",
)

# Create LangGraph Agent
agent_config = {
    "llm": llm,
    "tools": [retrieval_tool],
    "agent_type": AgentType.OPENAI_FUNCTIONS
}

agent = create_llm_agent(**agent_config)

# Define graph structure
graph = StateGraph(agent)
graph.add_edge(agent.END, agent.START)
graph.set_entry_point(agent.START)

rag_agent = graph.compile()
