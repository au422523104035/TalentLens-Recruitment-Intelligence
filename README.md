# TalentLens AI — Intelligent Recruitment Platform

An AI-driven recruitment intelligence platform designed to automate **resume screening, candidate-job matching, and skill gap analysis**. TalentLens AI helps recruiters evaluate candidates efficiently by extracting relevant information from resumes and providing transparent, explainable matching results.

## 🚀 Key Features

* 📄 **Resume Upload**

  * Supports PDF, DOCX, and TXT resume formats.

* 🔍 **Resume Information Extraction**

  * Extracts candidate name, contact details, education, experience, and technical skills.

* 💼 **Job Management**

  * Create and manage job descriptions with required skills.

* 🎯 **Candidate–Job Matching**

  * Ranks candidates against job roles using TF-IDF cosine similarity and skill-based scoring.

* 🧩 **Skill Gap Analysis**

  * Identifies matched skills and missing skills for each candidate.

* 📚 **Learning Recommendations**

  * Provides targeted recommendations to help candidates improve missing skills.

* 📊 **Explainable Results**

  * Displays transparent matching scores and the skills contributing to the result.

* 🗃️ **Local-First Architecture**

  * Uses SQLite and local NLP-style processing without requiring paid AI APIs.

## 🔄 System Workflow

```text
Resume Upload
      ↓
Resume Text Extraction
      ↓
Candidate Information & Skill Detection
      ↓
Job Role Selection
      ↓
Candidate–Job Matching
      ↓
Match Score & Skill Analysis
      ↓
Missing Skills & Learning Recommendations
```

## 🛠️ Technology Stack

### Frontend

* React
* Vite
* Tailwind CSS
* JavaScript

### Backend

* Python
* FastAPI
* SQLite
* PyPDF
* python-docx
* scikit-learn

### Matching

* TF-IDF Vectorization
* Cosine Similarity
* Skill-Based Matching

## 📁 Project Structure

```text
TalentLens-AI-Recruitment/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── parser.py
│   │   ├── database.py
│   │   └── skills.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## 💻 Run Locally

### 1. Start the Backend

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 2. Start the Frontend

Open another PowerShell terminal:

```powershell
cd frontend
npm install
npm run dev
```

Then open the local Vite URL shown in the terminal, usually:

```text
http://localhost:5173
```

## 🎓 Project Purpose

TalentLens AI is developed as a **CSE final-year project** demonstrating how intelligent automation and explainable matching techniques can improve the recruitment process.

The system focuses on reducing manual resume screening effort while providing recruiters with clear insights into candidate suitability and skill gaps.

## 🔮 Future Enhancements

* Advanced semantic resume matching using transformer-based models
* Multi-language resume processing
* Automated interview question generation
* Candidate ranking dashboards
* Recruiter authentication and role-based access
* Cloud deployment and scalable database support

## 📌 Project Status

**Development Status:** Functional Prototype

TalentLens AI currently provides resume upload, candidate extraction, job management, candidate-job matching, skill gap analysis, and learning recommendations through a local web application.

---

**TalentLens AI — Making Recruitment Smarter, Faster and More Explainable.**
