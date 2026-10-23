
import csv
from pathlib import Path

from llm_hybrid_test_cases import JOB_DESCRIPTION, TEST_CASES
from llm_hybrid_weak_resume_test import extract_evidence, calculate_score


def main():
    results = []

    for case in TEST_CASES:
        print(f"\n========== {case['name']} ==========")

        evidence = extract_evidence(case["resume"])
        score = calculate_score(evidence)
        expected = case["expected_score"]

        difference = round(score - expected, 2)

        print("Evidence:", evidence)
        print("Expected score:", expected)
        print("Actual score:", score)
        print("Difference:", difference)

        results.append([
            case["name"],
            evidence["Python"],
            evidence["SQL"],
            evidence["Data analysis"],
            expected,
            score,
            difference
        ])

    output_path = Path(__file__).with_name(
        "llm_hybrid_test_case_results.csv"
    )

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "test_case",
            "python_evidence",
            "sql_evidence",
            "data_analysis_evidence",
            "expected_score",
            "actual_score",
            "score_difference"
        ])
        writer.writerows(results)

    print("\n========== FINAL SUMMARY ==========")
    print("Test cases evaluated:", len(results))
    print("Results saved to:", output_path)


if __name__ == "__main__":
    main()
