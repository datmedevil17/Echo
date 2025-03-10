import pathway as pw

# Load indexed documents
doc_store = pw.xpacks.llm.document_store.DocumentStore.load("files-for-indexing")

def retrieve_documents(query: str):
    """Retrieve relevant documents using Pathway."""
    results = doc_store.query(query, top_k=5)
    return [doc.text for doc in results]
