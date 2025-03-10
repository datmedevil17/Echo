from fastapi import FastAPI, UploadFile, File
from agent import rag_agent
import asyncio

app = FastAPI()

@app.post("/ask")
async def ask_question(question: str):
    """Process user questions using LangGraph agent."""
    response = await asyncio.to_thread(rag_agent.invoke, question)
    return {"answer": response}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint for document upload."""
    with open(f"files-for-indexing/{file.filename}", "wb") as f:
        f.write(await file.read())
    return {"message": "File uploaded successfully!"}
