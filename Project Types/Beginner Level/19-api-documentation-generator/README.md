# API Documentation Generator from Code

## 📌 Project Overview
**Title:** API Documentation Generator from Code  
**Industry Category:** Engineering documentation maintenance and developer portals.  

### 📝 Description
Inspects backend API endpoints and functions to generate developer-friendly OpenAPI/Swagger specs and clean Markdown documentation.

---

## 💼 Enterprise & Industry Use Case
Engineering documentation maintenance and developer portals.

---

## 🎯 Interview Skills Tested
OpenAPI spec generation, schema deduction, technical documentation.

---

## 📦 Required Packages & Libraries
- `langchain-google-genai` (API schema analysis)
- `pydantic` (OpenAPI 3.0 schema modeling)
- `pyyaml` / `json` (Exporting swagger.yaml and OpenAPI specifications)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +--------------------+
| Backend Code /     | ----> | API Spec Generator   | ----> | OpenAPI 3.0 Spec & |
| Express Endpoints  |       |                      |       | Markdown Docs      |
+--------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Raw Controller / Route Code ] ──► [ AST / Route Endpoint Parser ]
                                                   │
                                                   ▼
                                       [ Gemini Spec Synthesizer ]
                                       - Extract HTTP Verb, Path, Query/Body
                                       - Document Status Codes (200, 400, 500)
                                                   │
                                                   ▼
                                       [ Validated OpenAPI 3.0 JSON / YAML ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Read Express/FastAPI route file: `app.post('/api/users', (req, res) => ...)`
2. LLM identifies request parameters, auth headers, and expected return types
3. Generate standard OpenAPI 3.0 schema YAML
4. Validate schema syntax using pyyaml
5. Write `openapi.yaml` and human-readable `API_REFERENCE.md`
```
