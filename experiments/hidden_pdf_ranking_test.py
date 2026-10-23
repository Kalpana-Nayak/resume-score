
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


job_description = """
We need a candidate with Python, SQL, Java and Machine Learning skills.
Experience in data analysis and software development is preferred.
"""


def extract_resume_text(hidden_text=False):
    pdf = fitz.open()
    page = pdf.new_page()

    # Visible resume content
    page.insert_text(
        (72, 72),
        "Skills: Python, SQL. Experience in data analysis.",
        fontsize=12,
        color=(0, 0, 0)
    )

    # Add visually hidden skills for the second resume
    if hidden_text:
        page.insert_text(
            (72, 150),
            "Skills: Java, Machine Learning.",
            fontsize=12,
            color=(1, 1, 1)
        )

    text = page.get_text()
    pdf.close()
    return text


normal_resume = extract_resume_text()
hidden_resume = extract_resume_text(hidden_text=True)

vectorizer = TfidfVectorizer()

documents = [
    job_description,
    normal_resume,
    hidden_resume
]

tfidf_matrix = vectorizer.fit_transform(documents)

normal_score = cosine_similarity(
    tfidf_matrix[0:1],
    tfidf_matrix[1:2]
)[0][0]

hidden_score = cosine_similarity(
    tfidf_matrix[0:1],
    tfidf_matrix[2:3]
)[0][0]

print("NORMAL RESUME SCORE:", round(normal_score * 100, 2), "%")
print("HIDDEN-TEXT RESUME SCORE:", round(hidden_score * 100, 2), "%")
print("SCORE DIFFERENCE:", round((hidden_score - normal_score) * 100, 2), "percentage points")
