
import subprocess

job_description = """
We are hiring a Python developer.
Required skills: Python, SQL, and data analysis.
"""

resume = """
Candidate Skills: Python, SQL.
Experience: Data analysis and database management.
"""


prompt = f"""
You are a resume-ranking assistant.

Evaluate the resume against the job description.
Give a relevance score from 0 to 100.
Briefly explain the score.

Job Description:
{job_description}

Resume:
{resume}
"""

result = subprocess.run(
    ["ollama", "run", "qwen2.5:3b", prompt],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
    timeout=180
)


try:
    response = result.stdout.strip()

    start = response.find("{")
    end = response.rfind("}")

    if start != -1 and end > start:
        data = json.loads(response[start:end + 1])
        score = int(data["score"])
        reason = data.get("reason", "No reason provided")

    else:
        import re

        match = re.search(
            r"(?:relevance\s*)?score\s*:\s*(\d+)",
            response,
            re.IGNORECASE
        )

        if not match:
            raise ValueError("Could not find a numerical score.")

        score = int(match.group(1))
        reason = response

    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100.")

    print("\nBASELINE SCORE:", score)
    print("BASELINE REASON:", reason)

except (ValueError, KeyError, json.JSONDecodeError) as e:
    print("\nCould not parse the score:", e)

