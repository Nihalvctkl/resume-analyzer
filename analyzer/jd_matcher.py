from analyzer.skill_extractor import extract_skills
from analyzer.score import calculate_score


def match_jd_with_resume(jd_text: str, resume_text: str, skills: list) -> dict:
    """
    Compare job description with resume.
    """
    jd_skills = extract_skills(jd_text, skills)
    resume_skills = extract_skills(resume_text, skills)

    score_result = calculate_score(resume_skills, jd_skills)
    missing_skills = list(set(jd_skills) - set(resume_skills))

    return {
        "jd_skills": jd_skills,
        "resume_skills": resume_skills,
        "missing_skills": missing_skills,
        "score": score_result
    }