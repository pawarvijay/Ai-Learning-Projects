# DevOps Incident Summary & Alert Bot

## 📌 Project Overview
**Title:** DevOps Incident Summary & Alert Bot  
**Industry Category:** SRE/DevOps on-call alerts and Datadog/PagerDuty log synthesis.  

### 📝 Description
Consumes raw server/cloud error logs, filters out repetitive noise, and formats a high-priority incident summary for Slack/Discord webhooks.

---

## 💼 Enterprise & Industry Use Case
SRE/DevOps on-call alerts and Datadog/PagerDuty log synthesis.

---

## 🎯 Interview Skills Tested
Log anomaly parsing, webhook JSON formatting, alert prioritization.

---

## 📦 Required Packages & Libraries
- `httpx` / `requests` (Posting payloads to Slack/Discord webhook URLs)
- `langchain-google-genai` (Log summarization and triage)
- `pydantic` (SlackBlockKit JSON payload schema)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +--------------------+
| Raw Cloud Server   | ----> | Incident Triage AI   | ----> | Actionable Slack / |
| Error Logs         |       |                      |       | Discord Alert Card |
+--------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Unstructured Server Logs ] ──► [ Error Deduplication & Grouping ]
                                                │
                                                ▼
                                    [ Gemini Incident Analyzer ]
                                    - Root Cause Hypothesis
                                    - Impact Assessment
                                    - Recommended First Step
                                                │
                                                ▼
                                    [ Slack BlockKit JSON Payload ]
                                                │
                                                ▼
                                    [ Webhook POST to #devops ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Ingest stack trace batch from cloud logs
2. Filter duplicate exception signatures
3. Send top anomalies to Gemini: "Synthesize into a 2-line incident alert with recommended immediate action."
4. Format output into Slack BlockKit JSON: {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": ...}}]}
5. httpx.post(SLACK_WEBHOOK_URL, json=payload) delivers alert directly to on-call engineers
```
