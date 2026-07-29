from utils.csv_report import generate_csv_report
from utils.ats_score import calculate_ats_score, get_recommendation
from utils.skill_matcher import find_skill_matches
from flask import Flask, render_template, request, send_file
import os

from utils.pdf_extractor import extract_text_from_pdf
from utils.text_preprocessor import preprocess_text
from utils.ranker import rank_resumes

app = Flask(__name__)
latest_ranked_resumes = []

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    # Get uploaded resumes
    files = request.files.getlist("resumes")

    # Get and preprocess job description
    job_description = request.form["job_description"]
    job_description = preprocess_text(job_description)

    resume_texts = []

    # Process each uploaded resume
    for file in files:

        if file.filename != "":

            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(file_path)

            # Extract text from PDF
            text = extract_text_from_pdf(file_path)

            # Clean the extracted text
            clean_text = preprocess_text(text)

            resume_texts.append({
                "filename": file.filename,
                "text": clean_text
            })

    # Rank resumes
    ranked_resumes = rank_resumes(
        job_description,
        resume_texts
    )

    for ranked_resume in ranked_resumes:
        for resume in resume_texts:
            if ranked_resume["filename"] == resume["filename"]:

                matched, missing = find_skill_matches(
                    job_description,
                    resume["text"]
                )

                ranked_resume["matched"] = matched
                ranked_resume["missing"] = missing

                ats_score = calculate_ats_score(
                    ranked_resume["score"],
                    matched,
                    missing
                )

                recommendation = get_recommendation(ats_score)

                ranked_resume["ats_score"] = ats_score
                ranked_resume["recommendation"] = recommendation

    # Generate CSV report
    generate_csv_report(ranked_resumes)

    global latest_ranked_resumes
    latest_ranked_resumes = ranked_resumes

    # Display results
    return render_template(
    "results.html",
    ranked_resumes=ranked_resumes
)
@app.route("/download-csv")
def download_csv():

    global latest_ranked_resumes

    if not latest_ranked_resumes:
        return "No report available."

    csv_file = generate_csv_report(latest_ranked_resumes)

    return send_file(
        csv_file,
        mimetype="text/csv",
        as_attachment=True,
        download_name="resume_ranking_report.csv"
    )

if __name__ == "__main__":
    app.run(debug=True)