import fitz  # PyMuPDF

def extract_pdf_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = []
    for page in doc:
        text.append(page.get_text("text"))
    return "\n".join(text).strip()
