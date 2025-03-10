import os
import pathway as pw
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

def process_document(file_path):
    """Parse, split, and store the uploaded document."""
    parser = pw.xpacks.llm.parsers.UnstructuredParser()
    splitter = pw.xpacks.llm.splitters.TokenCountSplitter(max_tokens=400)
    
    with open(file_path, "rb") as f:
        document_bytes = f.read()

    # Parse document
    parsed_docs = parser.parse(document_bytes)
    split_docs = splitter.split(parsed_docs)

    # Embed and store in retriever
    embedder = pw.xpacks.llm.embedders.SentenceTransformerEmbedder(model=config["EMBEDDING_MODEL"])
    retriever = pw.stdlib.indexing.BruteForceKnnFactory(
        reserved_space=1000, embedder=embedder, metric="cos", dimensions=1536
    ).create()
    
    retriever.insert([(doc.text,) for doc in split_docs])
    return retriever  # Store in memory

def get_relevant_context(retriever, query):
    """Retrieve top relevant document chunks based on query similarity."""
    results = retriever.search(query, k=3)
    return " ".join([doc[0] for doc in results])

def get_answer(retriever, query):
    """Fetch the answer from Mistral based on retrieved document context."""
    context = get_relevant_context(retriever, query)
    if not context:
        return "No relevant context found."

    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant answering questions based on provided documents."},
            {"role": "user", "content": f"Context: {context}\nQuestion: {query}"}
        ]
    }

    response = requests.post("https://api.mistral.ai/v1/chat/completions", json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No answer found.")
    
    return "Error fetching response from Mistral."
