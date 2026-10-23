
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


job_description = """
We need a candidate with Python and SQL skills.
Experience with data analysis and database management is required.
"""


def create_pdf(include_hidden_text=False):
    pdf = fitz.open()
    page = pdf.new_page()

    page.insert_text(
        (72, 72),
        "Skills: Python, SQL. Experience in data analysis and database management.",
        fontsize=12,
        color=(0, 0, 0)
    )

    if include_hidden_text:
        page.insert_text(
            (72, 150),
            "Skills: Java, Machine Learning",
            fontsize=12,
            color=(1, 1, 1)
        )

    return pdf


def extract_text(pdf, apply_defense=False):
    extracted_text = []

    for page in pdf:
        page_dict = page.get_text("dict")

        for block in page_dict["blocks"]:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    color = span["color"]

                    # Exclude white text when defense is enabled
                    if apply_defense and color == 16777215:
                        continue

                    if text:
                        extracted_text.append(text)

    return " ".join(extracted_text)


def calculate_score(resume_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(
        [job_description, resume_text]
    )

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return score * 100


normal_pdf = create_pdf(False)
hidden_pdf = create_pdf(True)

normal_text = extract_text(normal_pdf)
hidden_text = extract_text(hidden_pdf)
filtered_text = extract_text(hidden_pdf, apply_defense=True)

normal_score = calculate_score(normal_text)
hidden_score = calculate_score(hidden_text)
filtered_score = calculate_score(filtered_text)

print("NORMAL RESUME SCORE:", round(normal_score, 2), "%")
print("HIDDEN-TEXT RESUME SCORE:", round(hidden_score, 2), "%")
print("SCORE AFTER DEFENSE:", round(filtered_score, 2), "%")

print(
    "Hidden-text advantage:",
    round(hidden_score - normal_score, 2),
    "percentage points"
)

print(
    "Remaining advantage after defense:",
    round(filtered_score - normal_score, 2),
    "percentage points"
)

normal_pdf.close()
hidden_pdf.close()
