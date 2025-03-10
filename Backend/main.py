from fastapi import FastAPI, File, UploadFile, Query
from pathlib import Path
from qa_pipeline import process_document, get_answer

app = FastAPI()
UPLOAD_FOLDER = "files-for-indexing"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

# In-memory retriever
retriever = None

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global retriever
    file_path = Path(UPLOAD_FOLDER) / file.filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    retriever = process_document(file_path)
    return {"message": "File uploaded and processed successfully", "filename": file.filename}

@app.get("/ask")
async def ask_question(query: str = Query(..., description="Enter your question")):
    if retriever is None:
        return {"error": "No document uploaded. Please upload a file first."}

    answer = get_answer(retriever, query)
    return {"question": query, "answer": answer}
