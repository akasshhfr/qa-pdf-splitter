# Q&A PDF Splitter

A full-stack web app to **split** a combined Q&A PDF into separate question and answer PDFs, or **merge** two separate PDFs back into one.

## Features

- **Split** — Upload one PDF with numbered Q&As → get a ZIP with `questions.pdf` + `answers.pdf`
- **Merge** — Upload two separate PDFs (questions + answers) → get one combined PDF
- Dark-themed React UI with glassmorphism, tab navigation, drag-to-upload, loading states, and error handling

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| PDF Read | PyMuPDF |
| PDF Write | fpdf2 |
| Frontend | React, Vite |
| Styling | Vanilla CSS (Inter font, dark theme) |

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/upload` | Split a Q&A PDF → ZIP |
| POST | `/merge` | Merge two PDFs → combined PDF |

## Run Locally

**Backend** (terminal 1):

```powershell
cd backend
python -m venv ../.venv
../.venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend** (terminal 2):

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` — backend runs on `http://localhost:8000`.

## Supported Format

```
1. What is Python?
Ans: Python is a programming language.
```

Numbered questions (`1.`, `2.`, ...) followed by `Ans:` answers.

## Limitations

- Only supports `1. Question` / `Ans: Answer` format
- No OCR — text-based PDFs only