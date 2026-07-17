from dataclasses import dataclass
import re

from app.services.qa_parser import QuestionAnswer

@dataclass
class NumberedItem:
    number: int
    text: str

NUMBERED_ITEM_PATTERN = re.compile(
    r"(?m)^(\d+)\.\s+([\s\S]*?)(?=^\d+\.\s+|\Z)"
)

def parse_numbered_items(text:str) -> list[NumberedItem]:
    """Parse numbered items from text like '1. Some text here'."""

    if not text.strip():
        raise ValueError("Cannot parse empty text.")
    
    matches = NUMBERED_ITEM_PATTERN.findall(text)

    if not matches:
        raise ValueError(
            "No numbered item found."
            "Expected format: '1. Item text'"
        )
    
    items = []

    for number_str, content in matches:
        clean_text = " ".join(content.split())
        items.append(
            NumberedItem(
                number=int(number_str),
                text=clean_text,
            )
        )

    items.sort(key=lambda item: item.number)

    return items

def merge_questions_and_answers(
        questions: list[NumberedItem],
        answers: list[NumberedItem],
) -> list[QuestionAnswer]:
    """Match questions with answers by number. Return sorted pairs."""

    answer_map = {item.number: item.text for item in answers}

    merged = []

    for q in questions:
        answer_text = answer_map.get(q.number, "No answer found.")

        merged.append(
            QuestionAnswer(
                number=q.number,
                question=q.text,
                answer=answer_text,
            )
        )

    merged.sort(key=lambda item: item.number)

    return merged 