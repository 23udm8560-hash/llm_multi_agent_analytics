from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from xml.sax.saxutils import escape


def create_pdf_report(text: str, output_path: str):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(path), pagesize=letter, rightMargin=0.65*inch, leftMargin=0.65*inch, topMargin=0.65*inch, bottomMargin=0.65*inch)
    styles = getSampleStyleSheet()
    story = []
    for line in text.splitlines():
        safe = escape(line) or "&nbsp;"
        story.append(Paragraph(safe, styles["BodyText"]))
        story.append(Spacer(1, 4))
    doc.build(story)
    return str(path)
