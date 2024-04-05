import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

from docx import Document

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text




"""def extract_text_from_doc(doc_path):
    doc = fitz.open(doc_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

"""