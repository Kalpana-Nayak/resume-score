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
        "resume": "I have Python, Java, C, SQL and machine learning experience.",
        "expected_skills": ["python", "java", "c", "sql", "machine learning"]
    },
    {
        "name": "Substring trap",
        "resume": "I have experience in teamwork and communication.",
        "expected_skills": []
    },
    
    {
        "name": "Negated Java",
        "resume": "I have no experience with Java.",
        "expected_skills": []
    },
    {
        "name": "Negated Python",
        "resume": "I have never used Python.",
        "expected_skills": []
    },
    {
        "name": "Negated C",
        "resume": "I am not proficient in C.",
        "expected_skills": []
    },
    {
        "name": "Partial skills",
        "resume": "I know Python and SQL.",
        "expected_skills": ["python", "sql"]
    },
    {
        "name": "Alternative negation",
        "resume": "Java is not a skill I possess.",
        "expected_skills": []
    },
    {
        "name": "Lack of experience",
        "resume": "I lack Python experience.",
        "expected_skills": []
    },
    {
        "name": "Mixed positive and negative",
        "resume": "I have experience with Java, but not Python.",
        "expected_skills": ["java"]
    },
    {
        "name": "Basic experience",
        "resume": "I have basic Python experience.",
        "expected_skills": ["python"]
    },
    {
        "name": "Project experience",
        "resume": "I used Python in a project.",
        "expected_skills": ["python"]
    },
    
    {
        "name": "Repeated Python mention with negation",
        "resume": "Python is useful. I have no experience with Python.",
        "expected_skills": []
    },
    {
        "name": "Alternative Java negation",
        "resume": "I have never worked with Java.",
        "expected_skills": []
    },
    {
        "name": "Positive Python and negative Java",
        "resume": "I know Python, but I lack Java experience.",
        "expected_skills": ["python"]
    },
    {
        "name": "Python mentioned in reading context",
        "resume": "I enjoy reading about Python but have never used it.",
        "expected_skills": []
    },
    {
        "name": "Negative Java and positive Python",
        "resume": "I have no Java experience, but I use Python in projects.",
        "expected_skills": ["python"]
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


def calculate_metrics(true_positives, false_positives, false_negatives):
    if true_positives + false_positives == 0:
        precision = 0
    else:
        precision = true_positives / (true_positives + false_positives)

    if true_positives + false_negatives == 0:
        recall = 0
    else:
        recall = true_positives / (true_positives + false_negatives)

    if precision + recall == 0:
        f1_score = 0
    else:
        f1_score = 2 * precision * recall / (precision + recall)

    return precision, recall, f1_score


def evaluate_matcher_metrics(matcher):
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for case in TEST_CASES:
        resume = case["resume"]
        expected = case["expected_skills"]

        if matcher == original_matcher:
            matched, missing = matcher(JOB_DESCRIPTION, resume)
        else:
            matched, missing = matcher(
                JOB_DESCRIPTION, resume, SKILLS
            )

        expected_set = set(expected)
        matched_set = set(matched)

        true_positives += len(expected_set & matched_set)
        false_positives += len(matched_set - expected_set)
        false_negatives += len(expected_set - matched_set)

    precision, recall, f1_score = calculate_metrics(
        true_positives, false_positives, false_negatives
    )

    return (
        true_positives,
        false_positives,
        false_negatives,
        precision,
        recall,
        f1_score,
    )



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

    
    print("\nOVERALL MATCHER METRICS")

    for name, matcher in [
        ("Original", original_matcher),
        ("Boundary-aware", boundary_matcher),
        ("Negation-aware", negation_matcher),
    ]:
        tp, fp, fn, precision, recall, f1 = evaluate_matcher_metrics(matcher)

        print(f"\n{name} Matcher")
        print("True positives:", tp)
        print("False positives:", fp)
        print("False negatives:", fn)
        print(f"Precision: {precision:.2%}")
        print(f"Recall: {recall:.2%}")
        print(f"F1-score: {f1:.2%}")


    save_negation_results()

