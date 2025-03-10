import os
import pathway as pw
from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
from qa_pipeline import get_answer
from pathlib import Path

load_dotenv()
app = FastAPI()

UPLOAD_FOLDER = "files-for-indexing"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = Path(UPLOAD_FOLDER) / file.filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return {"message": "File uploaded successfully", "filename": file.filename}


@app.get("/ask")
async def ask_question(query: str):
    answer = get_answer(query)
    return {"question": query, "answer": answer}
