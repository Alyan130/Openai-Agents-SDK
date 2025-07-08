from fpdf import FPDF

class FormattedPDFReport(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font("Arial", size=12)

    def add_title(self, title):
        self.set_fill_color(70, 130, 180)  
        self.set_text_color(255, 255, 255)  
        self.set_font("Arial", 'B', 16)
        self.cell(0, 12, title, ln=True, align='C', fill=True)
        self.ln(8)
        self.set_text_color(0, 0, 0) 
        self.set_font("Arial", size=12)

    def add_section(self, heading, content):
        self.set_font("Arial", 'B', 14)
        self.set_draw_color(70, 130, 180) 
        self.cell(0, 10, heading, ln=True, border='B') 
        self.ln(2)
        self.set_font("Arial", size=12)
        self.multi_cell(0, 8, content)
        self.ln(4)

    def add_bullets(self, items):
        self.set_font("Arial", size=12)
        for item in items:
            self.cell(5) 
            self.multi_cell(0, 8, f"• {item}")
        self.ln(2)

def build_pdf(text: str) -> bytes:
    pdf = FormattedPDFReport()
    pdf.add_title("Profile Analysis Report")

    sections = text.split("\n\n")
    for sec in sections:
        lines = sec.strip().split("\n")
        if not lines:
            continue

        heading = lines[0].strip()
        content_lines = lines[1:]
        content = "\n".join(content_lines).strip()

        if all(l.strip().startswith("*") for l in content_lines if l.strip()):
            items = [l.strip("* ").strip() for l in content_lines]
            pdf.add_section(heading, "")
            pdf.add_bullets(items)
        else:
            pdf.add_section(heading, content)

    return pdf.output(dest='S').encode('latin-1')

