def calculate_ats_score(match_score, matched_skills, missing_skills):

    # Base score from similarity
    score = match_score

    # Reward matched skills
    score += len(matched_skills) * 5

    # Penalize missing skills
    score -= len(missing_skills) * 2

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    return round(score, 2)


def get_recommendation(score):

    if score >= 85:
        return "Excellent Match ⭐⭐⭐⭐⭐"

    elif score >= 70:
        return "Highly Suitable ⭐⭐⭐⭐"

    elif score >= 55:
        return "Good Match ⭐⭐⭐"

    elif score >= 40:
        return "Average Match ⭐⭐"

    else:
        return "Needs Improvement ⭐"