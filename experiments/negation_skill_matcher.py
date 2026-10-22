
import re


def contains_skill(text, skill):
    pattern = (
        r"(?<!\w)"
        + re.escape(skill.lower())
        + r"(?!\w)"
    )

    return re.search(pattern, text.lower()) is not None


def skill_is_negated(text, skill):
    text = text.lower()
    skill = skill.lower()

    pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

    for match in re.finditer(pattern, text):
        start = match.start()
        end = match.end()

        # Check the text immediately before the skill
        preceding_text = text[max(0, start - 60):start]

        # Check the text immediately after the skill
        following_text = text[end:end + 50]

        negation_before = [
            r"\bno experience with\s+$",
            r"\bno experience in\s+$",
            r"\bno knowledge of\s+$",
            r"\bnot skilled in\s+$",
            r"\bnot proficient in\s+$",
            r"\bnever used\s+$",
            r"\bwithout experience in\s+$",
            r"\black\s+$",
            r"\black experience with\s+$",
            r"\black experience in\s+$",
            r"\bnot\s+$",
        ]

        negation_after = [
            r"^\s+is not a skill\b",
            r"^\s+is not something I know\b",
            r"^\s+is not a skill I possess\b",
        ]

        if any(re.search(p, preceding_text) for p in negation_before):
            return True

        if any(re.search(p, following_text) for p in negation_after):
            return True

        # Handle: "Java, but not Python"
        if re.match(r"^\s*,?\s*but not\b", preceding_text[-20:]):
            return True

    return False



def find_skill_matches(job_description, resume_text, skills):
    matched = []
    missing = []

    for skill in skills:
        if contains_skill(job_description, skill):
            if (
                contains_skill(resume_text, skill)
                and not skill_is_negated(resume_text, skill)
            ):
                matched.append(skill)
            else:
                missing.append(skill)

    return matched, missing


if __name__ == "__main__":
    skills = ["c", "python", "java", "sql"]

    test_cases = [
        "I have Python and SQL experience.",
        "I have no experience with Java.",
        "I am not proficient in C.",
        "I have never used Python.",
    ]

    job_description = "Python, Java, C and SQL required."

    for resume in test_cases:
        matched, missing = find_skill_matches(
            job_description, resume, skills
        )

        print("\nResume:", resume)
        print("Matched:", matched)
        print("Missing:", missing)
