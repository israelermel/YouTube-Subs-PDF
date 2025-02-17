from fpdf import FPDF

class PDFCreator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=10)
        self.pdf.set_font("Arial", size=10)

    def create_pdf(self, text, filename):
        self.pdf.add_page()
        self.pdf.multi_cell(0, 10, text)
        self.pdf.output(filename)