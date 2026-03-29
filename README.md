# 🧠 AI Study Companion
### FastAPI + Google Gemini + Vercel

---

## Project Structure

```
study-companion/
├── api/
│   └── index.py          ← FastAPI backend (all AI logic lives here)
├── static/
│   └── index.html        ← Frontend (served by FastAPI)
├── requirements.txt      ← Python dependencies
├── vercel.json           ← Vercel deployment config
└── README.md
```

---

## Step 1 — Get your free Gemini API key

1. Go to → https://aistudio.google.com
2. Click **"Get API Key"** → **"Create API key"**
3. Copy the key (looks like: `AIzaSy...`)

No credit card required. Free forever for moderate usage.

---

## Step 2 — Run locally (test before deploying)

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export GEMINI_API_KEY="AIzaSy_your_key_here"   # Mac/Linux
set GEMINI_API_KEY=AIzaSy_your_key_here         # Windows

# Run the server
uvicorn api.index:app --reload

# Open in browser
# http://localhost:8000
```

---

## Step 3 — Deploy to Vercel

### 3a. Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/study-companion.git
git push -u origin main
```

### 3b. Deploy on Vercel

1. Go to → https://vercel.com → Sign up with GitHub
2. Click **"Add New Project"**
3. Import your `study-companion` repo
4. **Before clicking Deploy**, go to **"Environment Variables"** and add:
   - Key: `GEMINI_API_KEY`
   - Value: `AIzaSy_your_key_here`
5. Click **Deploy**
6. Your app is live at `your-project.vercel.app` 🎉

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Check if backend is running |
| POST | `/api/explain` | Get AI explanation of a topic |
| POST | `/api/quiz` | Generate a quiz from notes |
| GET | `/` | Serves the frontend |

### Example: /api/explain
```json
POST /api/explain
{
  "question": "What is gradient descent?",
  "notes": "your notes here...",
  "mode": "normal"
}
```

### Example: /api/quiz
```json
POST /api/quiz
{
  "notes": "your notes here...",
  "count": 5,
  "difficulty": "medium"
}
```

---

## Features

- 📝 **Notes** — Paste study material or pick a sample topic
- 💡 **Explain** — Ask anything in Normal / ELI5 / Deep Dive mode
- 🎯 **Quiz** — Auto-generated MCQ + Short Answer questions
- 📊 **Progress** — Tracks accuracy and flags weak topics

---

## Cost

- Vercel hosting → **Free**
- Gemini API → **Free** (no credit card needed)
- Total → **₹0**
