# Meeting Transcript Summarizer & Action Item Extractor

## 📌 Project Overview
**Title:** Meeting Transcript Summarizer & Action Item Extractor  
**Industry Category:** Post-meeting workflow automation for Zoom, Google Meet, and Slack.  

### 📝 Description
Processes conversational transcripts to produce executive summaries, key decisions, and assigned action item checklists.

---

## 💼 Enterprise & Industry Use Case
Post-meeting workflow automation for Zoom, Google Meet, and Slack.

---

## 🎯 Interview Skills Tested
Token budget management, entity extraction, markdown report generation.

---

## 📦 Required Packages & Libraries
- `langchain-core` (Prompts and LCEL chain pipeline)
- `langchain-google-genai` (Gemini Flash for large token context processing)
- `pydantic` (ActionItem schema with owner, task, and deadline)
- `python-docx` / `markdown` (Exporting meeting minutes to docx or markdown)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +--------------------+       +---------------------+
| Meeting Transcript | ----> | Transcript Parser  | ----> | Decisions, Summary  |
|   (Audio to Text)  |       |    & Synthesizer   |       | & Assigned Action Items|
+--------------------+       +--------------------+       +---------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Raw VTT/SRT Transcript ] ──► [ Transcript Cleaner / Normalizer ]
                                                  │
                                                  ▼
                                      [ Multi-Task Prompt Chain ]
                                      ├── Executive Summary Node
                                      ├── Decisions Made Node
                                      └── Action Items Extractor (Owner, Task)
                                                  │
                                                  ▼
                                      [ Structured Meeting Report ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. File loader reads meeting .vtt or plain text transcript
2. Clean noise: strip timestamps, speaker repetition artifacts
3. Prompt assembly:
   System: "Extract: 1. Executive Summary (3 bullets), 2. Decisions, 3. Action Items (Owner, Task, Deadline)"
4. LLM call: gemini-3.5-flash-lite.invoke(messages) with max_output_tokens=500
5. JsonOutputParser extracts ActionItem list: [{"owner": "Alex", "task": "Update AWS config", "due": "Friday"}]
6. Output written to markdown file or dispatched to Slack channel webhook
```
