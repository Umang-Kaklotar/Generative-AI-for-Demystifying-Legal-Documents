# ⚖️ Generative AI for Demystifying Legal Documents

## 📖 Overview
Legal documents are often **complex, lengthy, and difficult to interpret** for non-experts.  
This project — **Generative AI for Demystifying Legal Documents** — leverages **Google Gemini AI** to help users:

- 📂 Upload legal documents (PDF, DOCX, TXT)  
- ✨ Generate **simplified summaries**  
- ❓ Ask **natural language questions** about the document  
- 🔒 Access via a simple **login-protected frontend**  

The solution empowers individuals, businesses, and institutions to **understand legal content faster** and make **informed decisions**.

---

## 🎯 Solution Brief
The system is divided into two components:

1. **Backend (FastAPI + Gemini AI)**  
   - Handles authentication  
   - Extracts text from uploaded documents  
   - Generates summaries and answers using Gemini AI  

2. **Frontend (HTML, CSS, JavaScript)**  
   - Provides an intuitive UI  
   - Lets users log in, upload files, summarize, and ask questions  

---

## 📂 Project Structure

document-analyzer/
│
├── backend/
│ ├── app.py # FastAPI backend logic
│ ├── requirements.txt # Python dependencies
│ └── venv/ # Virtual environment (ignored in git)
│
└── frontend/
└── public/
├── index.html # Main UI
├── style.css # Styles
└── script.js   # Frontend logic
## 🛠️ Requirements

- **Python 3.10+**  
- **VS Code** with **Live Server extension**  
- A valid **Google Gemini API key**  

### Python Dependencies (`requirements.txt`)
fastapi
uvicorn
python-multipart
pdfplumber
python-docx
google-generativeai


---

## ⚙️ Installation (Backend)

```bash
# Clone repo
git clone https://github.com/your-username/document-analyzer.git
cd document-analyzer/backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows (PowerShell)

# Install dependencies
pip install -r requirements.txt
```
```
genai.configure(api_key="YOUR_GEMINI_API_KEY")
````
▶️ Running the Project
Start Backend
```
cd backend
uvicorn app:app --reload --host 127.0.0.1 --port 8000
````
```
API Docs: http://127.0.0.1:8000/docs
````
Start Frontend

Open frontend/public/index.html in VS Code

Right-click → Open with Live Server
```
Runs on http://127.0.0.1:5500
````
⚠️ The backend must be running before login or upload.

🔑 Default Login
````
Username: admin

Password: password123
````
🌟 Future Enhancements

Multi-user authentication system

Support for scanned image PDFs (OCR integration)

Advanced visualization of key clauses
