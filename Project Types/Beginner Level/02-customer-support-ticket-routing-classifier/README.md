# Customer Support Ticket Routing Classifier

## 📌 Project Overview
**Title:** Customer Support Ticket Routing Classifier  
**Industry Category:** Automated ticket triage for Zendesk, Jira Service Desk, and Freshdesk.  

### 📝 Description
Ingests customer support messages, classifies them into operational departments, and flags urgency priority with strict JSON output.

---

## 💼 Enterprise & Industry Use Case
Automated ticket triage for Zendesk, Jira Service Desk, and Freshdesk.

---

## 🎯 Interview Skills Tested
Few-shot intent classification, structured Pydantic output, latency optimization.

---

## 📦 Required Packages & Libraries
- `langchain-google-genai` (ChatGoogleGenerativeAI with structured output)
- `pydantic` (TicketClassification schema validation: category, priority, confidence)
- `fastapi` (REST API webhook endpoint receiving ticket submissions)
- `python-dotenv` (Secure environment key loading)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+----------------+       +----------------------+       +-----------------------+
| Support Ticket | ----> | AI Intent Classifier | ----> | Routed Department &   |
| (Raw Message)  |       |                      |       | Priority SLA (P1-P4)  |
+----------------+       +----------------------+       +-----------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Customer Email/Ticket ] ──► [ API Gateway / Webhook ]
                                         │
                                         ▼
                             [ Classification Prompt ]
                             - Categories: Billing, Tech, Account, General
                             - Priority Rules: P1 (Outage) to P4 (Low)
                                         │
                                         ▼
                             [ Gemini 3.5 Flash Lite ]
                                         │
                                         ▼
                             [ Pydantic JsonParser ] ──► [ Zendesk / Jira Route ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Incoming Webhook receives payload: {"ticket_id": "T-102", "body": "Cannot login, 500 error"}
2. Define Pydantic Schema:
   class TicketRoute(BaseModel):
       category: Literal['Billing', 'Technical', 'Account', 'General']
       priority: Literal['P1', 'P2', 'P3', 'P4']
       summary: str
       confidence: float
3. Model binding: llm.with_structured_output(TicketRoute)
4. Prompt invocation: ChatPromptTemplate with strict 0-shot classification guidelines
5. Response parsed directly into typed Python model without string regex
6. HTTP POST dispatched to downstream queue: router.forward(ticket.category, ticket.priority)
```
