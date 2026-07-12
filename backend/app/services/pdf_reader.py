from pathlib import Path

import pymupdf

def extract_text_from_pdf(pdf_path: str | Path) -> str:
    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    try:
        with pymupdf.open(path) as document:
            page_texts = [page.get_text() for page in document]
    except pymupdf.FileDataError as error:
        raise ValueError("The file is not a valid readable PDF.") from error

    extracted_text = "\n".join(page_texts)

    if not extracted_text.strip():
        raise ValueError(
            "No selected text was found. This may be a scanned PDF."
        )

    return extracted_text
