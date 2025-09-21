from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pdfplumber
import docx
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key="ENTER YOUR API KEY HERE")  # Replace with your Gemini API key

app = FastAPI()

# Allow frontend (Live Server) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Login credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return {"status": "success"}
    else:
        return {"status": "error", "message": "Invalid username or password"}

# Extract text from file
def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".txt"):
        with open(file_path, 'r', encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file format")
    return text

def preprocess_text(text):
    return " ".join(text.split())

def summarize_text(full_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
    "You are an AI legal assistant. Summarize this legal document clearly for a non-legal person. "
    "Follow the exact structure below, and make sure to use simple, clear, and professional language.\n\n"
    "Use this format:\n"
    "* Document type / main purpose: <one sentence>\n"
    "* Important dates / deadlines:\n"
    "  - <date + event>\n"
    "* Key obligations for the user:\n"
    "  - <obligation>\n"
    "* Rights of the user:\n"
    "  - <right>\n"
    "* Risks / red flags:\n"
    "  - <risk>\n"
    "* Practical advice / recommendations:\n"
    "  - <advice>\n\n"
    "Document:\n"
)

    response = model.generate_content(prompt + full_text)
    return response.text

def answer_question(full_text, question):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"You are an AI legal assistant. Answer based on this document:\n{full_text}\n\n"
        f"Question: {question}\nAnswer:"
    )
    response = model.generate_content(prompt)
    return response.text

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    try:
        full_text = preprocess_text(extract_text(file_location))
        os.remove(file_location)
        # only return extracted text (not summary yet)
        return {"text": full_text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/summarize")
async def summarize(text: str = Form(...)):
    try:
        summary = summarize_text(text)
        return {"summary": summary}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ask")
async def ask_question(question: str = Form(...), document: str = Form(...)):
    try:
        answer = answer_question(document, question)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
