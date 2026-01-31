from docx import Document

def parse_docx(file_path: str) -> str:
    """
    Extract text from a DOCX resume file.
    """
    text = ""

    try:
        document = Document(file_path)
        for para in document.paragraphs:
            if para.text:
                text += para.text + "\n"
    except Exception as e:
        print(f"[DOCX PARSER ERROR] {e}")

    return text
