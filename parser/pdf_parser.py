import pdfplumber

def parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF resume file.
    """
    extracted_text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
    except Exception as e:
        print(f"[PDF PARSER ERROR] {e}")

    return extracted_text