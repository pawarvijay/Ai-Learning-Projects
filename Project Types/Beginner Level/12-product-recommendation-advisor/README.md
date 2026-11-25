# E-Commerce Product Recommendation Advisor

## 📌 Project Overview
**Title:** E-Commerce Product Recommendation Advisor  
**Industry Category:** Online shopping assistants and retail personalized search.  

### 📝 Description
Matches customer preferences, budget, and constraints against a catalog of products (JSON) to suggest the top 3 best matching items with purchase justifications.

---

## 💼 Enterprise & Industry Use Case
Online shopping assistants and retail personalized search.

---

## 🎯 Interview Skills Tested
Content-based filtering, semantic catalog search, persuasive generation.

---

## 📦 Required Packages & Libraries
- `langchain-google-genai` (Gemini Flash Lite reasoning)
- `pydantic` (Product catalog and recommendation schemas)
- `json` (Catalog loading and query filtering)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+---------------------+       +----------------------+       +--------------------+
| Shopper Needs &     | ----> | Product Advisor AI   | ----> | Top 3 Products     |
| Budget Constraints  |       | (Catalog Grounded)   |       | with Reasons       |
+---------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ User Request / Budget ] ──┬──► [ Catalog Pre-Filter ] (Price <= Budget)
                            │                 │
[ Product Catalog JSON ] ───┘                 ▼
                                    [ Grounded Recommendation Prompt ]
                                              │
                                              ▼
                                    [ Gemini Flash Lite ]
                                              │
                                              ▼
                                    [ Top 3 Picks + Value Justification ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Load product catalog JSON: [{'id': 1, 'name': 'Laptop', 'price': 800, 'tags': ['lightweight']}]
2. Filter items strictly exceeding user budget ceiling
3. Pass filtered candidates + user preferences to LLM
4. LLM selects top 3 candidates and drafts a 1-sentence value pitch for each
5. Return structured recommendation card ready for frontend UI rendering
```
