from pathlib import Path

from app.services.pdf_reader import extract_text_from_pdf


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_PDF = PROJECT_ROOT / "backend" / "local_samples" / "sample.pdf"
OUTPUT_TEXT = PROJECT_ROOT / "backend" / "local_samples" / "extracted_text.txt"


def main() -> None:
    try:
        extracted_text = extract_text_from_pdf(INPUT_PDF)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        return

    OUTPUT_TEXT.write_text(extracted_text, encoding="utf-8")

    print(f"Text extracted successfully from: {INPUT_PDF}")
    print(f"Saved extracted text to: {OUTPUT_TEXT}")
    print("\nFirst 500 characters:\n")
    print(extracted_text[:500])


if __name__ == "__main__":
    main()