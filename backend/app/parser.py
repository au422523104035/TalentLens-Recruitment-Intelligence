import io
import re

from docx import Document
from pypdf import PdfReader

from .skills import extract_skills


def extract_text(filename: str, content: bytes) -> str:
    suffix = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    try:
        if suffix == "pdf":
            reader = PdfReader(io.BytesIO(content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif suffix == "docx":
            document = Document(io.BytesIO(content))
            text = "\n".join(p.text for p in document.paragraphs)
        elif suffix == "txt":
            text = content.decode("utf-8", errors="replace")
        else:
            raise ValueError("Only PDF, DOCX, and TXT resumes are supported.")
    except Exception as exc:
        raise ValueError("The uploaded file could not be read. Please upload a valid PDF, DOCX, or TXT resume.") from exc
    if len(text.strip()) < 20:
        raise ValueError("No readable text was found in this file. Please upload a text-based resume.")
    return text


def parse_candidate(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    email = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    phone = re.search(r"(?:\+?\d[\d\s().-]{7,}\d)", text)
    # Resumes commonly place the name in the first non-empty line.
    name = lines[0][:120] if lines else "Unnamed Candidate"
    education_lines = [line for line in lines if re.search(r"b\.?(tech|e|sc)|m\.?(tech|s|b|ca)|university|college|degree", line, re.I)]
    experience_lines = [line for line in lines if re.search(r"experience|intern|developer|engineer|analyst|year", line, re.I)]
    return {
        "name": name,
        "email": email.group(0) if email else "",
        "phone": phone.group(0) if phone else "",
        "education": " | ".join(education_lines[:3]),
        "experience": " | ".join(experience_lines[:4]),
        "skills": extract_skills(text),
    }
