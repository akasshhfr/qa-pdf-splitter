from pathlib import Path

from app.services.pdf_reader import extract_text_from_pdf
from app.services.qa_parser import split_questions_and_answers


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_PDF = PROJECT_ROOT / "backend" / "local_samples" / "sample.pdf"
EXTRACTED_TEXT = PROJECT_ROOT / "backend" / "local_samples" / "extracted_text.txt"
QUESTIONS_TEXT = PROJECT_ROOT / "backend" / "local_samples" / "questions.txt"
ANSWERS_TEXT = PROJECT_ROOT / "backend" / "local_samples" / "answers.txt"


def main() -> None:
    try:
        extracted_text = extract_text_from_pdf(INPUT_PDF)
        question_answers = split_questions_and_answers(extracted_text)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        return

    EXTRACTED_TEXT.write_text(extracted_text, encoding="utf-8")

    questions_only = "\n\n".join(
    f"{index}. {item.question}"
    for index, item in enumerate(question_answers, start=1)
    )

    answers_only = "\n\n".join(
    f"{index}. {item.answer}"
    for index, item in enumerate(question_answers, start=1)
    )

    QUESTIONS_TEXT.write_text(questions_only, encoding="utf-8")
    ANSWERS_TEXT.write_text(answers_only, encoding="utf-8")

    print(f"Found {len(question_answers)} question-answer pairs.")
    print(f"Questions saved to: {QUESTIONS_TEXT}")
    print(f"Answers saved to: {ANSWERS_TEXT}")
    print("\nFirst question:")
    print(questions_only.split("\n\n")[0])

if __name__ == "__main__":
    main()


# task1: to sort the questions and answers in serial number ✅
# task2: i give questions and answers seperrately, it should combine them with the correct answer match (given serial number for bith Q & A)
# task3: task2 should also be in sorted order, numerically
# task4: make a question paper generator
# task5: calculate the time taken to seperate/merge 2000 questions with answers of 7 lines each (make a noting of time taken to seperate or merge)
# task6: try to make task5 efficient 
