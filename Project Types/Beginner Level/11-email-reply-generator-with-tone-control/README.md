# Smart Email Drafter with Tone Modulation

## 📌 Project Overview
**Title:** Smart Email Drafter with Tone Modulation  
**Industry Category:** Executive inbox productivity and sales outreach automation.  

### 📝 Description
Drafts contextual email responses based on incoming thread context, allowing the user to select tones (Professional, Friendly, Concise, Urgent).

---

## 💼 Enterprise & Industry Use Case
Executive inbox productivity and sales outreach automation.

---

## 🎯 Interview Skills Tested
Tone modulation, prompt templating, contextual chaining.

---

## 📦 Required Packages & Libraries
- `langchain-core` (ChatPromptTemplate with tone parameter)
- `langchain-google-genai` (Gemini Flash Lite generator)
- `pydantic` (EmailDraft schema validation)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +--------------------+
| Incoming Email &   | ----> | Contextual Email     | ----> | Ready-to-Send      |
| Selected Tone      |       | Drafter              |       | Tailored Email     |
+--------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Email Thread Context ] ──┬──► [ Prompt Template ]
                           │          - Tone parameter (Formal / Casual / Urgent)
[ Desired Tone / Intent ] ─┘          - Key points to include
                                                │
                                                ▼
                                    [ Gemini 3.5 Flash Lite ]
                                                │
                                                ▼
                                    [ Formatted Subject + Body ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Ingest thread context: sender, original message, user's key reply bullet points
2. User specifies tone: Enum['Formal', 'Friendly', 'Direct', 'Negotiation']
3. Prompt template applies stylistic few-shot instructions matching target tone
4. Gemini generates response enforcing concise business communication standards
5. Output returns structured draft: {"subject": str, "body": str, "sign_off": str}
```
