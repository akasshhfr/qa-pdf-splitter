import tempfile
import zipfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse

from app.services.pdf_reader import extract_text_from_pdf
from app.services.qa_parser import split_questions_and_answers
from app.services.pdf_writer import generate_pdf

app = FastAPI(
    title="Q&A PDF Splitter API",
    description="API for separating questions and answers from a PDF.",
    version="0.1.0",
)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "Q&A PDF Splitter API is running",
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile) -> FileResponse:
    """Accept a PDF upload, extract Q&A, return a ZIP with two PDFs."""

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted."
        )
    
    temp_dir = tempfile.mkdtemp() #temporary path for processing the file
    temp_dir_path = Path(temp_dir)

    try:
        input_pdf_path = temp_dir_path / "uploaded.pdf"
        contents = await file.read()
        input_pdf_path.write_bytes(contents)

        try:
            extracted_text = extract_text_from_pdf(input_pdf_path)
            qa_pairs = split_questions_and_answers(extracted_text)
        except (FileNotFoundError, ValueError) as error:
            raise HTTPException(status_code=400, detail=str(error))
        
        questions_pdf_path = temp_dir_path / "questions.pdf"
        answers_pdf_path = temp_dir_path / "answers.pdf"

        generate_pdf(qa_pairs, questions_pdf_path, content_type="questions")
        generate_pdf(qa_pairs, answers_pdf_path, content_type="answers")

        zip_path = temp_dir_path / "qa_results.zip" #creating a zip file

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.write(questions_pdf_path, arcname="questions.pdf") #arcname is file name
            zf.write(answers_pdf_path, arcname="answers.pdf")

        return FileResponse(
            path = str(zip_path),
            filename="qa_results.zip",
            media_type="application/zip",
        )
    
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occured: {error}",
        )