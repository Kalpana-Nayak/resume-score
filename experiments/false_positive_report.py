
from compare_matchers import original_matcher
from defended_skill_matcher import find_skill_matches as boundary_matcher
from negation_skill_matcher import find_skill_matches as negation_matcher
from evaluate_defenses import TEST_CASES, JOB_DESCRIPTION, SKILLS

matchers = [
    ("Original", original_matcher),
    ("Boundary-aware", boundary_matcher),
    ("Negation-aware", negation_matcher)
]

for name, matcher in matchers:
    print("\n" + "=" * 50)
    print(name, "Matcher")
    print("=" * 50)

    total_false_positives = 0

    for case in TEST_CASES:
        resume = case["resume"]
        expected = set(case["expected_skills"])

        if matcher == original_matcher:
            matched, missing = matcher(JOB_DESCRIPTION, resume)
        else:
            matched, missing = matcher(JOB_DESCRIPTION, resume, SKILLS)

        false_positives = sorted(set(matched) - expected)

        if false_positives:
            total_false_positives += len(false_positives)
            print("\nResume:", resume)
            print("Incorrectly detected skills:", false_positives)

    print("\nTotal false positives:", total_false_positives)
