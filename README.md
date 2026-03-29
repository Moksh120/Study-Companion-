#  AI Study Companion

An AI-powered study tool that explains topics, generates quizzes, and tracks your weak areas — built with Python (FastAPI) and Google Gemini.

---

## Features

- **📝 Notes** — Paste study material or upload a PDF (up to 10 MB)
- **💡 Explain** — Ask any question about your notes in three modes:
  - Normal — clear explanation with examples
  - ELI5 — simplified for beginners
  - Deep Dive — technical depth and theory
- **🎯 Quiz** — Auto-generates MCQ and short answer questions from your notes with adjustable difficulty (Easy / Medium / Hard)
- **📊 Progress** — Tracks your accuracy per topic and flags weak areas

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| AI | Google Gemini 2.5 Flash |
| PDF Parsing | pdfplumber |
| Frontend | HTML, CSS, Vanilla JS |
| Deployment | Vercel |

---

## Project Structure

```
ai/
├── api/
│   └── index.py        ← FastAPI backend (all AI logic)
├── static/
│   └── index.html      ← Frontend UI
├── requirements.txt    ← Python dependencies
├── vercel.json         ← Vercel deployment config
├── .env                ← API key (did not commit)
├── .gitignore
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check if backend is running and key is set |
| POST | `/api/explain` | Get AI explanation of a topic |
| POST | `/api/quiz` | Generate a quiz from notes |
| POST | `/api/upload-pdf` | Upload and extract text from a PDF |
| GET | `/` | Serves the frontend |



## Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/ai.git
cd ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Gemini API key
Go to [aistudio.google.com](https://aistudio.google.com) → Get API Key → Create API key in new project. No credit card required.

### 4. Create a `.env` file
```
GEMINI_API_KEY=your_key_here
```

### 5. Run the server
```bash
uvicorn api.index:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### 6. Verify it's working
Visit [http://localhost:8000/api/health](http://localhost:8000/api/health) — you should see:
```json
{"status": "ok", "key_set": true}
```

