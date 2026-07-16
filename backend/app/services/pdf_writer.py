from pathlib import Path
from fpdf import FPDF
from app.services.qa_parser import QuestionAnswer

def generate_pdf(
        items: list[QuestionAnswer],
        output_path:str | Path,
        content_type: str,
) -> Path:
     """Generate a PDF containing only questions or only answers."""

     path = Path(output_path)

     pdf = FPDF()
     pdf.set_auto_page_break(auto=True, margin=20)
     pdf.add_page()
     pdf.set_font("Helvetica", size=12)

     title = "Questions" if content_type == "questions" else "Answers"
     pdf.set_font("Helvetica", style="B", size=18)
     pdf.cell(text=title, new_x="LEFT", new_y="NEXT")
     pdf.ln(10)

     pdf.set_font("Helvetica", size=12)

     for item in items:
          number = item.number
          text = item.question if content_type == "questions" else item.answer

          label = f"{number}. "

          pdf.set_font("Helvetica", style="B", size=12)
          label_width = pdf.get_string_width(label)
          pdf.cell(w=label_width, text=label)

          pdf.set_font("Helvetica", size=12)
          page_width = pdf.w - pdf.l_margin - pdf.r_margin
          remaining_width = page_width - label_width
          pdf.multi_cell(w=remaining_width, text=text)

          pdf.ln(4)

     pdf.output(str(path))
     return path