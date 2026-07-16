# Q&A PDF Splitter

A web application that accepts a PDF containing questions and answers, then creates two separate PDFs:

- Questions only
- Answers only

## Current progress

- Part 1 complete: FastAPI backend foundation and health-check endpoint.
- Part 2 complete: PDF text extraction using PyMuPDF.
- Part 3 complete: Parsed numbered questions and answers into separate text files.
- Part 4 complete: PDF generation with fpdf2 and `/upload` API endpoint.
## Tech stack

- Python
- FastAPI
- Uvicorn
- React (planned)

## Run the backend locally

1. Create and activate the virtual environment.

2. Install dependencies:

   ```powershell
   python -m pip install -r backend\requirements.txt