
import fitz


def create_pdf(include_hidden_text=False):
    pdf = fitz.open()
    page = pdf.new_page()

    # Visible resume content
    page.insert_text(
        (72, 72),
        "Skills: Python, SQL",
        fontsize=12,
        color=(0, 0, 0)
    )

    # Suspicious white-on-white text
    if include_hidden_text:
        page.insert_text(
            (72, 150),
            "Skills: Java, Machine Learning",
            fontsize=12,
            color=(1, 1, 1)
        )

    return pdf


def inspect_pdf(pdf):
    suspicious_text = []

    for page in pdf:
        page_dict = page.get_text("dict")

        for block in page_dict["blocks"]:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    color = span["color"]

                    # PyMuPDF represents white as 16777215
                    if text and color == 16777215:
                        suspicious_text.append(text)

    return suspicious_text


for name, include_hidden in [
    ("Normal PDF", False),
    ("PDF with hidden text", True)
]:
    pdf = create_pdf(include_hidden)
    detected = inspect_pdf(pdf)

    print("\nTest:", name)
    print("Suspicious text detected:", detected)
    print("Defense flag:", bool(detected))

    pdf.close()


print("\nDEFENSE EVALUATION")

test_cases = [
    ("Normal PDF", False, False),
    ("PDF with hidden text", True, True)
]

correct = 0

for name, has_hidden_text, expected_flag in test_cases:
    pdf = create_pdf(has_hidden_text)
    detected = inspect_pdf(pdf)
    actual_flag = bool(detected)

    result = "CORRECT" if actual_flag == expected_flag else "INCORRECT"

    print(name, "->", result)

    if actual_flag == expected_flag:
        correct += 1

    pdf.close()

accuracy = correct / len(test_cases) * 100

print("Correct classifications:", correct, "out of", len(test_cases))
print("Classification accuracy:", round(accuracy, 2), "%")

