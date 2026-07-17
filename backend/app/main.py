import tempfile
import zipfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse

from app.services.pdf_reader import extract_text_from_pdf
from app.services.qa_parser import split_questions_and_answers
from app.services.pdf_writer import generate_pdf, generate_combined_pdf
from app.services.item_parser import parse_numbered_items, merge_questions_and_answers

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
    
@app.post("/merge")
async def merge_pdfs(
    question_file: UploadFile,
    answer_file: UploadFile,
) -> FileResponse:
    """Accept two PDFs, merge into one combined pdf"""

    for f in [question_file, answer_file]:
        if f.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail=f"Only PDF files are accepted. '{f.filename} is not a PDF."
            )
        
    temp_dir = tempfile.mkdtemp()
    temp_dir_path = Path(temp_dir)

    try:
        q_path = temp_dir_path / "questions_input.pdf"
        a_path = temp_dir_path / "answers_input.pdf"
        q_contents = await question_file.read()
        q_path.write_bytes(q_contents)
        a_contents = await answer_file.read()
        a_path.write_bytes(a_contents)
        try:
            q_text = extract_text_from_pdf(q_path)
            a_text = extract_text_from_pdf(a_path)
        except (FileNotFoundError, ValueError) as error:
            raise HTTPException(status_code=400, detail=str(error))
        try:
            question_items = parse_numbered_items(q_text)
            answer_items = parse_numbered_items(a_text)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error))
        merged = merge_questions_and_answers(question_items, answer_items)
        combined_path = temp_dir_path / "combined_qa.pdf"
        generate_combined_pdf(merged, combined_path)
        return FileResponse(
            path=str(combined_path),
            filename="combined_qa.pdf",
            media_type="application/pdf",
        )
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {error}",
        )