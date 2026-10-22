import sys
import os
import csv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from defended_skill_matcher import find_skill_matches as boundary_matcher
from negation_skill_matcher import find_skill_matches as negation_matcher

SKILLS = ["python", "java", "c", "sql", "machine learning"]

TEST_CASES = [
    {
        "name": "Valid skills",
        "resume": "I have Python, Java, C, SQL and machine learning experience."
    },
    {
        "name": "Substring trap",
        "resume": "I have experience in teamwork and communication."
    },
    {
        "name": "Negated Java",
        "resume": "I have no experience with Java."
    },
    {
        "name": "Negated Python",
        "resume": "I have never used Python."
    },
    {
        "name": "Negated C",
        "resume": "I am not proficient in C."
    },
    {
        "name": "Partial skills",
        "resume": "I know Python and SQL."
    },
    {
        "name": "Alternative negation",
        "resume": "Java is not a skill I possess."
    },
    {
        "name": "Lack of experience",
        "resume": "I lack Python experience."
    },
    {
        "name": "Mixed positive and negative",
        "resume": "I have experience with Java, but not Python."
    },
    {
        "name": "Basic experience",
        "resume": "I have basic Python experience."
    },
    {
        "name": "Project experience",
        "resume": "I used Python in a project."
    }

]

JOB_DESCRIPTION = (
    "Python, Java, C, SQL and machine learning skills are required."
)


def original_matcher(job_description, resume):
    jd = job_description.lower()
    text = resume.lower()
    matched = []
    missing = []

    for skill in SKILLS:
        if skill in jd:
            if skill in text:
                matched.append(skill)
            else:
                missing.append(skill)

    return matched, missing




def count_negation_errors(matcher):
    cases = [
        ("I have no experience with Java.", "java"),
        ("I have never used Python.", "python"),
        ("I am not proficient in C.", "c"),
        ("Java is not a skill I possess.", "java"),
        ("I lack Python experience.", "python"),
        ("I have experience with Java, but not Python.", "python"),
    ]

    errors = 0

    for resume, skill in cases:
        if matcher == original_matcher:
            matched, missing = matcher(JOB_DESCRIPTION, resume)
        else:
            matched, missing = matcher(
                JOB_DESCRIPTION, resume, SKILLS
            )

        if skill in matched:
            errors += 1

    return errors



def save_negation_results():
    matchers = [
        ("Original", original_matcher),
        ("Boundary-aware", boundary_matcher),
        ("Negation-aware", negation_matcher),
    ]

    cases = [
        ("Negated Java", "I have no experience with Java.", "java"),
        ("Negated Python", "I have never used Python.", "python"),
        ("Negated C", "I am not proficient in C.", "c"),
    ]

    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "negation_results.csv"
    )

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Test", "Matcher", "Target Skill", "False Positive"
        ])

        for name, resume, skill in cases:
            for matcher_name, matcher in matchers:
                if matcher_name == "Original":
                    matched, missing = matcher(JOB_DESCRIPTION, resume)
                else:
                    matched, missing = matcher(
                        JOB_DESCRIPTION, resume, SKILLS
                    )

                false_positive = skill in matched

                writer.writerow([
                    name,
                    matcher_name,
                    skill,
                    false_positive
                ])

    print(f"\nSaved results to: {output_path}")



def run_evaluation():
    for case in TEST_CASES:
        print("\n" + "=" * 50)
        print("Test:", case["name"])
        print("Resume:", case["resume"])

        original_matched, original_missing = original_matcher(
            JOB_DESCRIPTION, case["resume"]
        )

        boundary_matched, boundary_missing = boundary_matcher(
            JOB_DESCRIPTION, case["resume"], SKILLS
        )

        negation_matched, negation_missing = negation_matcher(
            JOB_DESCRIPTION, case["resume"], SKILLS
        )

        print("\nOriginal matcher")
        print("Matched:", original_matched)
        print("Missing:", original_missing)

        print("\nBoundary-aware matcher")
        print("Matched:", boundary_matched)
        print("Missing:", boundary_missing)

        print("\nNegation-aware matcher")
        print("Matched:", negation_matched)
        print("Missing:", negation_missing)


def evaluate_positive_cases(matcher):
    cases = [
        ("I have Python, Java, C, SQL and machine learning experience.",
         ["python", "java", "c", "sql", "machine learning"]),
        ("I know Python and SQL.",
         ["python", "sql"]),
        ("I have basic Python experience.",
         ["python"]),
        ("I used Python in a project.",
         ["python"]),
        ("I have experience with Java, but not Python.",
         ["java"]),
    ]

    false_negatives = 0
    total_expected_skills = 0

    for resume, expected_skills in cases:
        if matcher == original_matcher:
            matched, missing = matcher(JOB_DESCRIPTION, resume)
        else:
            matched, missing = matcher(JOB_DESCRIPTION, resume, SKILLS)

        for skill in expected_skills:
            total_expected_skills += 1

            if skill not in matched:
                false_negatives += 1

    return false_negatives, total_expected_skills



if __name__ == "__main__":
    run_evaluation()
    print("\nNEGATION ERROR SUMMARY")
    print("Boundary-aware errors:", count_negation_errors(boundary_matcher))
    print("Negation-aware errors:", count_negation_errors(negation_matcher))

    print("\nFALSE NEGATIVE SUMMARY")

    for name, matcher in [
        ("Original", original_matcher),
        ("Boundary-aware", boundary_matcher),
        ("Negation-aware", negation_matcher),
    ]:
        errors, total = evaluate_positive_cases(matcher)
        print(f"{name}: {errors} false negatives out of {total} expected skills")

    save_negation_results()

