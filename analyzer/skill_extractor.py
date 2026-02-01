def load_skills(file_path: str) -> list:
    """
    Load skills from a text file.
    """
    skills = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            skills = [line.strip().lower() for line in file if line.strip()]
    except Exception as e:
        print(f"[SKILL LOADER ERROR] {e}")

    return skills


import re

def extract_skills(resume_text: str, skills: list) -> list:
    """
    Extract skills using word-boundary matching.
    """
    found_skills = []

    for skill in skills:
        # Escape special characters like c++
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, resume_text):
            found_skills.append(skill)

    return found_skills
