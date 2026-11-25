# Resume & Job Description Matcher (ATS Screener)

## 📌 Project Overview
**Title:** Resume & Job Description Matcher (ATS Screener)  
**Industry Category:** Applicant Tracking Systems (ATS) and automated HR candidate screening.  

### 📝 Description
Evaluates candidate resumes against job specifications to score compatibility, missing technical skills, and candidate strengths.

---

## 💼 Enterprise & Industry Use Case
Applicant Tracking Systems (ATS) and automated HR candidate screening.

---

## 🎯 Interview Skills Tested
Semantic vector similarity, structured evaluation rubrics, resume parsing.

---

## 📦 Required Packages & Libraries
- `pypdf` / `docx2txt` (Parsing multi-format resume files)
- `scikit-learn` (Cosine similarity between dense embedding vectors)
- `langchain-google-genai` (Deep qualitative skill gap analysis)
- `pydantic` (CandidateEvaluation report schema)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+-----------------+       +-------------------+       +--------------------+
| Resume (PDF) &  | ----> | ATS Matcher &     | ----> | Match Score (%),   |
| Job Description |       | Qualitative Grader|       | Skill Gaps & Verdict|
+-----------------+       +-------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Resume Text ] ────────► [ Dense Embedder ] ──┐
                                               ▼
[ Job Description Text ] ► [ Dense Embedder ] ─► [ Cosine Similarity Score (0-100%) ]
                                               │
                                               ▼
                                  [ Qualitative Gap Evaluator ]
                                  - Missing Must-Have Skills
                                  - Candidate Strengths & Weaknesses
                                               │
                                               ▼
                                  [ Candidate Scorecard ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Parse resume (pypdf/docx2txt) and extract normalized text
2. Embed resume and JD text using GoogleGenerativeAIEmbeddings
3. Calculate baseline cosine similarity: dot(res_vec, jd_vec) / (norm(res) * norm(jd))
4. Pass both texts to Gemini LLM with rubric:
   "Identify: 1. Matched Required Skills, 2. Missing Skills, 3. Interview Questions"
5. Parse output into CandidateReview Pydantic schema
6. Combine mathematical semantic score (40%) + qualitative LLM grade (60%) into final ranking
```
