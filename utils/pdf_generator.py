from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from datetime import datetime
from reportlab.platypus import Image
import os


def generate_final_plan_pdf(final_text,logo_path=None, filename="marketing_plan.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    content = []

    if logo_path and os.path.exists(logo_path):
        content.append(Image(logo_path, width=150, height=150))
        content.append(Spacer(1, 20))

    # Title
    content.append(Paragraph("📈 Marketing Strategy Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(
        Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"])
    )
    content.append(Spacer(1, 20))

    # Split sections (basic formatting)
    sections = final_text.split("\n")

    for line in sections:
        line = line.strip()

        if not line:
            continue

        # Detect headings
        if ":" in line and len(line) < 60:
            content.append(Paragraph(f"<b>{line}</b>", styles["Heading3"]))
        else:
            content.append(Paragraph(line, styles["BodyText"]))

        content.append(Spacer(1, 10))

    doc.build(content)

    return filename
