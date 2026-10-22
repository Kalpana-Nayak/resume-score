
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from utils.skill_matcher import find_skill_matches as original_matcher
from experiments.defended_skill_matcher import (
    find_skill_matches as defended_matcher
)

skills = [
    "c",
    "python",
    "java",
    "sql",
    "machine learning"
]

job_description = """
Looking for C programming, Python, Java, SQL,
and machine learning skills.
"""

test_cases = [
    {
        "name": "Valid skills",
        "text": "Python, Java, SQL and machine learning."
    },
    {
        "name": "Substring trap",
        "text": "I have experience and communication skills."
    },
    {
        "name": "Keyword stuffing",
        "text": "Python Python Python SQL SQL SQL."
    },
    {
        "name": "Negated skill",
        "text": "I have no experience with Java."
    }
]

for case in test_cases:
    print("\nTest:", case["name"])

    old_matched, old_missing = original_matcher(
        job_description, case["text"]
    )

    new_matched, new_missing = defended_matcher(
        job_description, case["text"], skills
    )

    print("Original matched:", old_matched)
    print("Defended matched:", new_matched)
    print("Original missing:", old_missing)
    print("Defended missing:", new_missing)
