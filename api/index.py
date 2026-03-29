from dotenv import load_dotenv
load_dotenv()

import os
import io
import json
import httpx
import pdfplumber
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# ── Request models ────────────────────────────────────────────────────────────

class ExplainRequest(BaseModel):
    question: str
    notes: str = ""
    mode: str = "normal"  # normal | eli5 | deep

class QuizRequest(BaseModel):
    notes: str
    count: int = 5
    difficulty: str = "medium"  # easy | medium | hard


# ── Helper ────────────────────────────────────────────────────────────────────

async def call_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set in environment variables.")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=f"Gemini API error: {resp.text}")

    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "key_set": bool(GEMINI_API_KEY)}


@app.post("/api/explain")
async def explain(req: ExplainRequest):
    mode_instructions = {
        "normal": "Give a clear, well-structured explanation with examples.",
        "eli5":   "Explain this like I am 10 years old. Use very simple language, fun analogies, and relatable examples. Avoid jargon completely.",
        "deep":   "Give a deep, comprehensive explanation including underlying theory, edge cases, and connections to other concepts. Include technical depth."
    }

    note_context = f"\n\nStudent's notes:\n---\n{req.notes[:3000]}\n---\n" if req.notes.strip() else ""

    prompt = f"""You are a brilliant study tutor. {mode_instructions.get(req.mode, mode_instructions['normal'])}
{note_context}
Student's question: {req.question}

Format your response clearly. Use line breaks for readability. If relevant, include a short example.
Use **bold** for key terms."""

    answer = await call_gemini(prompt)
    return {"answer": answer}


@app.post("/api/quiz")
async def quiz(req: QuizRequest):
    notes_text = req.notes.strip() or "General computer science and programming concepts."

    prompt = f"""You are a quiz generator. Based on the following study notes, create {req.count} quiz questions at {req.difficulty} difficulty level.

Notes:
---
{notes_text[:3000]}
---

Create a mix of MCQ and short answer questions.
Return ONLY valid JSON (no markdown, no explanation, no code fences), in this exact format:
{{
  "topic": "detected topic name (short, 2-4 words)",
  "questions": [
    {{
      "type": "mcq",
      "question": "question text",
      "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
      "correct": "A) option1",
      "explanation": "brief explanation why"
    }},
    {{
      "type": "short",
      "question": "question text",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "model_answer": "ideal concise answer"
    }}
  ]
}}"""

    raw = await call_gemini(prompt)

    # Strip markdown code fences if Gemini wraps in them
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()

    try:
        quiz_data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse quiz JSON from Gemini response.")

    return quiz_data


# ── PDF Upload ────────────────────────────────────────────────────────────────

@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Read file bytes
    contents = await file.read()

    
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="PDF too large. Please upload a file under 10 MB.")

    # Extract text with pdfplumber
    text = ""
    page_count = 0
    try:
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read PDF: {str(e)}")

    text = text.strip()

    if not text:
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from this PDF. It may be a scanned image PDF. Please copy-paste the text manually."
        )

    # Cap extracted text at 8000 chars to stay within Gemini context limits
    truncated = len(text) > 8000
    text = text[:8000]

    return {
        "text": text,
        "page_count": page_count,
        "char_count": len(text),
        "truncated": truncated,
        "filename": file.filename,
    }


# ── Serve frontend ────────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")
