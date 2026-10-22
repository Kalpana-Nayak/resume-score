
import re


def contains_skill(text, skill):
    text = text.lower().strip()
    skill = skill.lower().strip()

    pattern = (
        r"(?<!\w)"
        + re.escape(skill)
        + r"(?!\w)"
    )

    return re.search(pattern, text) is not None


def find_skill_matches(job_description, resume_text, skills):
    matched = []
    missing = []

    for skill in skills:
        if contains_skill(job_description, skill):
            if contains_skill(resume_text, skill):
                matched.append(skill)
            else:
                missing.append(skill)

    return matched, missing


if __name__ == "__main__":
    skills = ["c", "python", "machine learning"]

    resume = (
        "I have experience with Python and "
        "machine learning."
    )

    matched, missing = find_skill_matches(
        "C programming, Python, machine learning",
        resume,
        skills
    )

    print("Matched:", matched)
    print("Missing:", missing)
