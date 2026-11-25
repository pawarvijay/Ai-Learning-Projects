# Multi-Platform Social Media Content Repurposer

## 📌 Project Overview
**Title:** Multi-Platform Social Media Content Repurposer  
**Industry Category:** Marketing automation and content creation workflows.  

### 📝 Description
Converts a single blog post or article into tailored copy for LinkedIn, X/Twitter, and Instagram with platform-specific formatting.

---

## 💼 Enterprise & Industry Use Case
Marketing automation and content creation workflows.

---

## 🎯 Interview Skills Tested
Persona prompting, platform character constraints, multi-output pipelines.

---

## 📦 Required Packages & Libraries
- `langchain-core` (Prompt formatting and branching)
- `langchain-google-genai` (Creative multi-format generation)
- `pydantic` (MultiPlatformPost schema with character limit validation)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +---------------------+
| Blog Post / Article| ----> | Content Repurposer   | ----> | LinkedIn, X Thread, |
|                    |       |                      |       | & Instagram Copy    |
+--------------------+       +----------------------+       +---------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Long-Form Blog Post ] ──► [ Core Message Extractor ]
                                         │
                                         ▼
                     ┌───────────────────┼───────────────────┐
                     ▼                   ▼                   ▼
             [ LinkedIn Node ]    [ X Thread Node ]  [ Instagram Node ]
             - Professional tone  - Hook + 5 tweets  - Visual caption
             - Formatting spacing - <280 chars each  - Hashtags
                     │                   │                   │
                     └───────────────────┼───────────────────┘
                                         ▼
                             [ Multi-Channel Bundle ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Ingest article string and extract primary thesis
2. Run single LLM pass with structured schema returning 3 platform variants
3. Enforce validation: X tweets must not exceed 280 characters
4. LinkedIn post includes thought-leadership hook and call-to-action
5. Output structured JSON ready for social media scheduler APIs (Buffer/Hootsuite)
```
