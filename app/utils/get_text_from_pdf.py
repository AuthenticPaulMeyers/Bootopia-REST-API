# extract text from the PDFs
import pdfplumber

def extract_text_content(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "".join([page.extract_text()
        for page in pdf.pages])
    return text


# Todo: extract text from scanned documents