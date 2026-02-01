import os

from parser.pdf_parser import parse_pdf
from parser.docx_parser import parse_docx
from utils.cleaner import clean_text
from analyzer.skill_extractor import load_skills, extract_skills
from analyzer.score import calculate_score


def read_resume(file_path: str) -> str:
    """
    Detect resume type and extract raw text.
    """
    if file_path.lower().endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return parse_docx(file_path)
    else:
        raise ValueError("Unsupported resume format")


def main():
    resume_path = "sample.docx"   # change to .docx if needed
    skills_path = os.path.join("data", "skills.txt")

    raw_text = read_resume(resume_path)
    cleaned_text = clean_text(raw_text)
    
    required_skills = load_skills(skills_path)
    found_skills = extract_skills(cleaned_text, required_skills)

    result = calculate_score(found_skills, required_skills)

    print("Resume Analysis Result")
    print("----------------------")
    print(f"Matched Skills : {found_skills}")
    print(f"Score          : {result['score']}%")
    print(f"Match Details  : {result}")


if __name__ == "__main__":
    main()

