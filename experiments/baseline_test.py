
import sys
from pathlib import Path

# Allow imports from the project root
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from utils.ranker import rank_resumes
from utils.skill_matcher import find_skill_matches
from utils.ats_score import calculate_ats_score

job_description = """
Python developer with experience in Flask, SQL, Docker,
Azure, REST API development and Git.
"""

original_resume = """
Information Technology student.
Completed a Python project using Flask and SQL.
Familiar with Git and REST API development.
"""

keyword_stuffed_resume = """
Information Technology student.
Completed a Python project using Flask and SQL.
Familiar with Git and REST API development.

Python Python Python Flask Flask SQL SQL Docker Docker
Azure Azure Azure REST API REST API Git Git Git.
"""

resumes = [
    {
        "filename": "original",
        "text": original_resume
    },
    {
        "filename": "keyword_stuffed",
        "text": keyword_stuffed_resume
    }
]

ranked = rank_resumes(job_description, resumes)

print("\n=== BASELINE EXPERIMENT ===")

for result in ranked:
    filename = result["filename"]
    match_score = result["score"]

    resume_text = (
        original_resume
        if filename == "original"
        else keyword_stuffed_resume
    )

    matched, missing = find_skill_matches(
        job_description, resume_text
    )

    ats_score = calculate_ats_score(
        match_score, matched, missing
    )

    print(f"\nResume: {filename}")
    print(f"Match score: {match_score}%")
    print(f"ATS score: {ats_score}%")
    print(f"Matched skills: {matched}")
    print(f"Missing skills: {missing}")
