def generate_feedback(missing_skills):

    feedback = []

    for skill in missing_skills:

        feedback.append(f"Consider learning or adding '{skill}' to improve your resume.")

    if not feedback:
        feedback.append("Excellent! Your resume matches all the required skills.")

    return feedback