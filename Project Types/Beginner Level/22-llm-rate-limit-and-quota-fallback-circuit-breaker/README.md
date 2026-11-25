# LLM Rate Limit & Quota Circuit Breaker (Resilience)

## 📌 Project Overview
**Title:** LLM Rate Limit & Quota Circuit Breaker (Resilience)  
**Industry Category:** High-availability enterprise LLM infrastructure, resilient production APIs.  

### 📝 Description
Handles API provider rate limits (HTTP 429), quota exhaustion, and vendor downtime by automatically falling back to secondary models with exponential backoff and jitter.

---

## 💼 Enterprise & Industry Use Case
High-availability enterprise LLM infrastructure, resilient production APIs.

---

## 🎯 Interview Skills Tested
Circuit breaker pattern, exponential backoff, multi-model fallback chains (`with_fallbacks`).

---

## 📦 Required Packages & Libraries
- `langchain-google-genai` (Primary model client)
- `tenacity` (Robust retries, exponential backoff, jitter, and stop conditions)
- `pydantic` (Fallback event logging schema)

---

## ⚠️ Real-World Edge Cases & Failure Modes
- **Critical Failure Mode:** Production outages, runaway token bills, and prompt injection exploits.
- **Defensive Mechanism:** Built specifically to catch, isolate, and mitigate failure modes before they reach core business logic.

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +--------------------+
| Application Request| ----> | Resilient Circuit    | ----> | Zero-Downtime      |
|                    |       | Breaker & Fallback   |       | Continuous Response|
+--------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Incoming Request ] ──► [ Primary Model: Gemini 3.5 Flash ]
                                         │
                             ┌───────────┴───────────┐
                             ▼ (Success)             ▼ (HTTP 429 / Out of Quota)
                      [ Return 200 ]          [ Circuit Breaker Tripped ]
                                                     │
                                                     ▼
                                              [ Exponential Backoff + Jitter ]
                                                     │
                                                     ▼
                                              [ Fallback Model: Gemini Flash Lite ]
                                                     │
                                                     ▼
                                              [ Resilient Return 200 ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Define primary: ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
2. Define fallbacks: primary.with_fallbacks([ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite"), ChatGoogleGenerativeAI(model="gemini-3.6-flash")])
3. Wrap with Tenacity retry policy: stop_after_attempt(3), wait_exponential_jitter(initial=1, max=10)
4. On HTTP 429 / QuotaExceeded error, catch exception, increment metrics, switch model transparently
5. Return successfully generated content without user experiencing 500 error
```
