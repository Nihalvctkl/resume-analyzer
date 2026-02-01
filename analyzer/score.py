def calculate_score(found_skills: list, required_skills: list) -> dict:
    """
    Calculate resume score based on skill match.
    """
    if not required_skills:
        return {
            "matched": 0,
            "total": 0,
            "percentage": 0,
            "score": 0
        }

    matched_skills = set(found_skills) & set(required_skills)
    matched_count = len(matched_skills)
    total_required = len(required_skills)

    percentage = (matched_count / total_required) * 100
    score = round(percentage)

    return {
        "matched": matched_count,
        "total": total_required,
        "percentage": round(percentage, 2),
        "score": score
    }