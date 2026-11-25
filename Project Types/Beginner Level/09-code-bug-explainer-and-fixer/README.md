# Code Bug Explainer & Auto-Fixer

## 📌 Project Overview
**Title:** Code Bug Explainer & Auto-Fixer  
**Industry Category:** Developer tooling, CI/CD automated triage, and coding education.  

### 📝 Description
Takes buggy code snippets alongside error tracebacks, diagnoses the root cause, and generates corrected code patches with explanations.

---

## 💼 Enterprise & Industry Use Case
Developer tooling, CI/CD automated triage, and coding education.

---

## 🎯 Interview Skills Tested
Code reasoning, traceback parsing, diff/patch generation.

---

## 📦 Required Packages & Libraries
- `langchain-core` (Structured prompt templates)
- `langchain-google-genai` (Code reasoning with Gemini)
- `pydantic` (BugDiagnosis schema with root cause, fix, and explanation)
- `rich` (Syntax-highlighted terminal diff rendering)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+---------------------+       +----------------------+       +----------------------+
| Buggy Code &        | ----> | AI Debugger & Code   | ----> | Root Cause Diagnosis |
| Error Traceback     |       | Repair Engine        |       | & Verified Fix Patch |
+---------------------+       +----------------------+       +----------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Buggy Snippet + Stack Trace ] ──► [ Prompt with Language Context ]
                                                    │
                                                    ▼
                                        [ Gemini Reasoning Model ]
                                                    │
                                                    ▼
                                        [ Structured Diagnosis ]
                                        ├── Root Cause Explanation
                                        ├── Corrected Code Block
                                        └── Preventive Recommendations
                                                    │
                                                    ▼
                                        [ Developer Terminal / PR ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Collect runtime error trace + faulty code function
2. Construct Prompt: "Analyze this stack trace. Explain the bug in 2 sentences and return the fixed code."
3. Send to Gemini Flash Lite with temperature=0.1 for high code determinism
4. Parse response into markdown blocks: `Explanation` and `Fixed Code`
5. Print diff to developer using rich.syntax.Syntax
```
