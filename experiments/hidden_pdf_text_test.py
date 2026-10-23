
import fitz

pdf = fitz.open()
page = pdf.new_page()

# Visible resume content
page.insert_text(
    (72, 72),
    "Name: Test Candidate\nSkills: Python, SQL",
    fontsize=12,
    color=(0, 0, 0)
)

# Visually hidden text: white font on a white page
page.insert_text(
    (72, 150),
    "Skills: Java, Machine Learning",
    fontsize=12,
    color=(1, 1, 1)
)

# Extract the text
extracted_text = page.get_text()

print("EXTRACTED PDF TEXT:")
print(extracted_text)

print("\nSKILL DETECTION:")
print("Python detected:", "Python" in extracted_text)
print("SQL detected:", "SQL" in extracted_text)
print("Java detected:", "Java" in extracted_text)
print("Machine Learning detected:", "Machine Learning" in extracted_text)

pdf.close()
