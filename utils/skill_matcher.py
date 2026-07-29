SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "javascript",
    "typescript",
    "react",
    "angular",
    "vue",
    "node",
    "express",
    "flask",
    "django",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "linux",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "tensorflow",
    "pytorch",
    "numpy",
    "pandas",
    "opencv",
    "scikit-learn",
    "rest api",
    "api",
    "firebase"
]


def find_skill_matches(job_description, resume_text):

    job_description = job_description.lower()
    resume_text = resume_text.lower()

    matched = []
    missing = []

    for skill in SKILLS:

        if skill in job_description:

            if skill in resume_text:
                matched.append(skill)
            else:
                missing.append(skill)

    return matched, missing