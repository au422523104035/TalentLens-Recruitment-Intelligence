from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Candidate, Job
from .parser import extract_text, parse_candidate
from .skills import extract_skills, recommendations_for


def serialize_candidate(candidate: Candidate) -> dict:
    return {"id": candidate.id, "name": candidate.name, "email": candidate.email, "phone": candidate.phone,
            "education": candidate.education, "experience": candidate.experience,
            "skills": [s for s in candidate.skills.split(",") if s], "source_filename": candidate.source_filename,
            "created_at": candidate.created_at.isoformat()}


def serialize_job(job: Job) -> dict:
    return {"id": job.id, "title": job.title, "company": job.company, "location": job.location,
            "description": job.description, "required_skills": [s for s in job.required_skills.split(",") if s],
            "created_at": job.created_at.isoformat()}


def seed_data(db: Session):
    if db.query(Job).count() == 0:
        jobs = [
            Job(title="Junior Full Stack Developer", company="NovaTech", location="Chennai / Hybrid",
                description="Build web applications with React, JavaScript, Python, FastAPI, SQL, Git, HTML and CSS. Work in an Agile team.",
                required_skills="react,javascript,python,fastapi,sql,git,html,css,agile"),
            Job(title="Data Analyst Intern", company="InsightWorks", location="Remote",
                description="Analyse business data using Python, SQL, Excel, pandas, Power BI, data analysis and Tableau.",
                required_skills="python,sql,excel,pandas,data analysis,power bi,tableau"),
            Job(title="Machine Learning Engineer", company="Aster AI", location="Bengaluru",
                description="Develop machine learning and NLP solutions using Python, scikit-learn, pandas, numpy, Docker and AWS.",
                required_skills="python,machine learning,nlp,scikit-learn,pandas,numpy,docker,aws"),
        ]
        db.add_all(jobs)
    if db.query(Candidate).count() == 0:
        text = """Aarav Kumar\naarav.kumar@example.com | +91 98765 43210\nB.Tech Computer Science, Chennai\nSkills: Python, JavaScript, React, HTML, CSS, SQL, Git, FastAPI, SQLite, pandas\nProjects: Built a React dashboard and FastAPI REST API.\nExperience: Software Developer Intern, 6 months."""
        parsed = parse_candidate(text)
        db.add(Candidate(**{**parsed, "skills": ",".join(parsed["skills"]), "resume_text": text, "source_filename": "aarav-kumar-demo.txt"}))
    db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_data(db)
    finally:
        db.close()
    yield


app = FastAPI(title="TalentLens AI API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    # Support direct browser calls as well as the Vite development proxy.
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JobInput(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    company: str = Field(default="", max_length=160)
    location: str = Field(default="Remote", max_length=120)
    description: str = Field(min_length=20)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/jobs")
def list_jobs(db: Annotated[Session, Depends(get_db)]):
    return [serialize_job(job) for job in db.query(Job).order_by(Job.created_at.desc()).all()]


@app.post("/api/jobs", status_code=201)
def create_job(payload: JobInput, db: Annotated[Session, Depends(get_db)]):
    skills = extract_skills(payload.description)
    job = Job(**payload.model_dump(), required_skills=",".join(skills))
    db.add(job); db.commit(); db.refresh(job)
    return serialize_job(job)


@app.get("/api/candidates")
def list_candidates(db: Annotated[Session, Depends(get_db)]):
    return [serialize_candidate(candidate) for candidate in db.query(Candidate).order_by(Candidate.created_at.desc()).all()]


@app.post("/api/candidates/upload", status_code=201)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(400, "Please select a resume file.")
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(413, "Resume must be smaller than 5 MB.")
    try:
        text = extract_text(file.filename, content)
        parsed = parse_candidate(text)
    except (ValueError, OSError, EOFError) as exc:
        raise HTTPException(400, str(exc)) from exc
    candidate = Candidate(**{**parsed, "skills": ",".join(parsed["skills"]), "resume_text": text, "source_filename": file.filename})
    db.add(candidate); db.commit(); db.refresh(candidate)
    return serialize_candidate(candidate)


@app.get("/api/matches/{candidate_id}/{job_id}")
def match_candidate(candidate_id: int, job_id: int, db: Annotated[Session, Depends(get_db)]):
    candidate = db.get(Candidate, candidate_id)
    job = db.get(Job, job_id)
    if not candidate or not job:
        raise HTTPException(404, "Candidate or job was not found.")
    candidate_skills = set(filter(None, candidate.skills.split(",")))
    required = set(filter(None, job.required_skills.split(",")))
    matched = sorted(candidate_skills & required)
    missing = sorted(required - candidate_skills)
    skill_score = (len(matched) / len(required) * 100) if required else 0
    matrix = TfidfVectorizer(stop_words="english").fit_transform([candidate.resume_text, job.description])
    text_score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100)
    score = round(0.7 * skill_score + 0.3 * text_score)
    return {"candidate": serialize_candidate(candidate), "job": serialize_job(job), "match_score": score,
            "skill_coverage": round(skill_score), "text_similarity": round(text_score), "matched_skills": matched,
            "missing_skills": missing, "recommendations": recommendations_for(missing),
            "methodology": "70% required-skill coverage + 30% TF-IDF cosine similarity of resume and job text."}
