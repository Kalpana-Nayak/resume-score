import csv
import io


def generate_csv_report(ranked_resumes):

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Rank",
        "Resume Name",
        "Match Score",
        "ATS Score",
        "Recommendation",
        "Matched Skills",
        "Missing Skills"
    ])

    for rank, resume in enumerate(ranked_resumes, start=1):

        writer.writerow([
            rank,
            resume["filename"],
            f"{resume['score']}%",
            f"{resume['ats_score']}/100",
            resume["recommendation"],
            ", ".join(resume["matched"]),
            ", ".join(resume["missing"])
        ])

    output.seek(0)
    

    csv_bytes = io.BytesIO(output.getvalue().encode("utf-8"))

    return csv_bytes
