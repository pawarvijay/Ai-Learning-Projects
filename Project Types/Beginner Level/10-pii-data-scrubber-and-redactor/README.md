# PII Data Scrubber & Anonymizer

## 📌 Project Overview
**Title:** PII Data Scrubber & Anonymizer  
**Industry Category:** Compliance (GDPR, HIPAA) and enterprise AI safety gateways.  

### 📝 Description
Detects and redacts Personally Identifiable Information (Emails, Phone Numbers, Credit Cards, SSNs) from input text before downstream LLM processing.

---

## 💼 Enterprise & Industry Use Case
Compliance (GDPR, HIPAA) and enterprise AI safety gateways.

---

## 🎯 Interview Skills Tested
Regex + LLM hybrid detection, data masking, safety guardrails.

---

## 📦 Required Packages & Libraries
- `re` (Fast regex pre-filtering for standard patterns like SSN, email, credit card)
- `langchain-google-genai` (Context-aware entity detection for names and addresses)
- `pydantic` (Masking configuration and audit log schemas)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+---------------------+       +----------------------+       +----------------------+
| Raw Sensitive Text  | ----> | PII Redaction        | ----> | Safe Anonymized Text |
| (Contains PII/GDPR) |       | Firewall             |       | (Ready for LLM APIs) |
+---------------------+       +----------------------+       +----------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Raw User Input ] ──► [ Fast Regex Filter ] (Emails, Phone, SSN)
                                      │
                                      ▼
                        [ LLM Contextual Scrubber ] (Names, Addresses, Identifiers)
                                      │
                                      ▼
                        [ Masked Output: <REDACTED_EMAIL>, <REDACTED_NAME> ]
                                      │
                                      ▼
                        [ Downstream Cloud LLM / Logs ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Pass input string through compiled regex: re.sub(EMAIL_REGEX, '<EMAIL>', text)
2. Run contextual NLP/LLM pass for ambiguous entities (e.g. personal names, medical IDs)
3. Generate token replacement map: {'John Doe': '<USER_1>', 'San Jose': '<CITY_1>'}
4. Replace occurrences while retaining grammatical readability
5. Return anonymized payload alongside audit log of redacted entity types
```
