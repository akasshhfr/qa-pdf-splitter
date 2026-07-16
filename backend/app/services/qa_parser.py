from dataclasses import dataclass
import re

@dataclass
class QuestionAnswer:
    number: int
    question: str
    answer: str

QUESTION_ANSWER_PATTERN = re.compile(
    r"(?m)^Q?(\d+)\.\s+(.+?)\s*\nAns:\s([\s\S]*?)(?=^Q?\d+\.\s+|\Z)"
)

def split_questions_and_answers(text:str) -> list[QuestionAnswer]:
    if not text.strip():
        raise ValueError("Cannot split empty text.")
    
    matches = QUESTION_ANSWER_PATTERN.findall(text)

    if not matches:
        raise ValueError(
            "No question-answer pairs found."
            "Expected numbered questions followed by 'Ans:'."
        )
    
    question_answer = []

    for number, question, answer in matches:
        clean_question = " ".join(question.split())
        clean_answer = " ".join(answer.split())

        question_answer.append(
            QuestionAnswer(
                number=int(number),
                question=clean_question,
                answer=clean_answer,
            )
        )
    
    question_answer.sort(key=lambda item: item.number)

    return question_answer