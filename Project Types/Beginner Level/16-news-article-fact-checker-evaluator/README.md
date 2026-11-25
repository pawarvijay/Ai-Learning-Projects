# Article Fact-Checker & Hallucination Evaluator

## 📌 Project Overview
**Title:** Article Fact-Checker & Hallucination Evaluator  
**Industry Category:** LLMOps quality evaluation and automated journalism compliance.  

### 📝 Description
Compares an AI-generated summary against source facts to detect fabricated claims, scoring factual consistency from 1 to 10.

---

## 💼 Enterprise & Industry Use Case
LLMOps quality evaluation and automated journalism compliance.

---

## 🎯 Interview Skills Tested
Evaluator-Optimizer pattern, LLM-as-a-judge, claim verification.

---

## 📦 Required Packages & Libraries
- `langchain-google-genai` (LLM-as-a-judge evaluator)
- `pydantic` (FactCheckResult schema with consistency score and flagged hallucinations)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+---------------------+       +----------------------+       +--------------------+
| Generated Summary & | ----> | LLM Fact-Checker     | ----> | Faithfulness Score |
| Ground-Truth Facts  |       | (Judge)              |       | (1-10) & Audit Log |
+---------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Ground-Truth Article ] ──┬──► [ Claim Extraction Engine ]
                           │                │
[ AI-Generated Summary ] ──┘                ▼
                                 [ Cross-Verification Matrix ]
                                 - Check every claim in summary
                                 - Flag unsupported assertions
                                            │
                                            ▼
                                 [ Faithfulness Scorecard ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Break summary into discrete atomic propositions: ["Company founded in 2020", "Raised $5M"]
2. For each proposition, verify whether ground truth source text explicitly entails it
3. LLM evaluates: ENTAILED | CONTRADICTED | NOT_MENTIONED (Hallucination)
4. Calculate faithfulness score: (entailed_claims / total_claims) * 10
5. Output report with flagged hallucinations highlighted for human review
```
