"""Small local skill lexicon and explainable matching helpers."""
import re

SKILL_CATALOG = [
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "react", "angular",
    "vue", "node.js", "express", "fastapi", "django", "flask", "html", "css", "tailwind css",
    "sql", "mysql", "postgresql", "sqlite", "mongodb", "firebase", "rest api", "graphql",
    "git", "github", "docker", "kubernetes", "aws", "azure", "linux", "figma",
    "machine learning", "deep learning", "data analysis", "data structures", "algorithms",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "nlp", "power bi", "tableau",
    "excel", "agile", "scrum", "testing", "pytest", "selenium", "cybersecurity",
]

RECOMMENDATIONS = {
    "react": "Build a small React dashboard and practise components, state, and routing.",
    "fastapi": "Complete a FastAPI CRUD API project and learn request validation with Pydantic.",
    "python": "Practise Python fundamentals, data structures, and a small automation project.",
    "sql": "Learn SQL joins, aggregation, and schema design using SQLite or PostgreSQL.",
    "machine learning": "Study supervised learning, evaluation metrics, and complete a scikit-learn project.",
    "docker": "Containerise a small web application and learn images, volumes, and Compose.",
    "aws": "Learn IAM, EC2, S3, and deploy a small static or API project.",
    "git": "Practise branching, pull requests, merges, and a clean Git workflow.",
}


def extract_skills(text: str) -> list[str]:
    normalized = text.lower().replace("nodejs", "node.js")
    found = []
    for skill in SKILL_CATALOG:
        # Word boundaries prevent e.g. 'java' matching 'javascript'.
        pattern = r"(?<![\w+#.])" + re.escape(skill) + r"(?![\w+#.])"
        if re.search(pattern, normalized, flags=re.IGNORECASE):
            found.append(skill)
    return sorted(found)


def recommendations_for(missing: list[str]) -> list[dict]:
    return [
        {"skill": skill, "recommendation": RECOMMENDATIONS.get(skill, f"Follow a focused beginner course and build a portfolio project using {skill.title()}.")}
        for skill in missing[:5]
    ]
