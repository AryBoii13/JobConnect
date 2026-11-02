"""Resume text extraction and keyword-based skill parsing.

This is intentionally a transparent, rule-based matcher rather than
a machine-learning model: it is easy to explain in a review and easy
to extend (just add words to SKILLS_VOCAB). Swapping this out for a
smarter extractor later is a drop-in change — only extract_skills()
needs to change, nothing that calls it.
"""
import re

from pypdf import PdfReader

# A starter vocabulary — extend this as your project grows.
SKILLS_VOCAB = [
    "python", "java", "c++", "c", "javascript", "typescript", "sql", "r",
    "django", "flask", "fastapi", "react", "angular", "vue", "node.js", "node",
    "html", "css", "bootstrap", "tailwind",
    "pandas", "numpy", "matplotlib", "scikit-learn", "tensorflow", "pytorch",
    "machine learning", "deep learning", "data analysis", "data visualization",
    "git", "github", "docker", "kubernetes", "linux", "rest api", "graphql",
    "mysql", "postgresql", "sqlite", "mongodb", "firebase",
    "aws", "azure", "gcp",
    "excel", "power bi", "tableau",
    "communication", "leadership", "teamwork", "problem solving",
]


def extract_text(file_field) -> str:
    """Pull plain text out of an uploaded resume (.pdf or .txt)."""
    name = file_field.name.lower()
    file_field.open("rb")
    try:
        if name.endswith(".pdf"):
            reader = PdfReader(file_field)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        return file_field.read().decode("utf-8", errors="ignore")
    finally:
        file_field.close()


def extract_skills(text: str) -> list[str]:
    """Return the subset of SKILLS_VOCAB that appears in `text`,
    matched as whole words/phrases, case-insensitively."""
    text_lower = text.lower()
    found = []
    for skill in SKILLS_VOCAB:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text_lower):
            found.append(skill)
    return found
