# 40,000 Feet Architecture: High-Level System View

```
                  [ User Request ]
                         │
                         ▼
┌─────────────────────────────────────────────────┐
│                    LangGraph                    │ ◄── Orchestrator (Loops, State Machine)
│           (Runs 1 Agent or a "Swarm")           │
└────────────────────────┬────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────┐
│                      Agent                      │ ◄── Brain / Worker (Decides what to do)
└───────┬────────────────┼────────────────┬───────┘
        │                │                │
        ▼                ▼                ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   LangChain   │ │      RAG      │ │   MCP / Tool  │ ◄── Tool Plug
│ (Prompts &    │ │  (Reads PDFs  │ └───────┬───────┘
│  Glue Code)   │ │  & VectorDB)  │         │ (Calls API)
└───────┬───────┘ └───────────────┘         ▼
        │                           ┌───────────────┐
        ▼                           │    Node.js    │ ◄── Your Service
┌───────────────┐                   │    Service    │
│      LLM      │                   └───────┬───────┘
│  (GPT/Claude/ │                           │ (SQL Query)
│    Gemini)    │                           ▼
└───────────────┘                   ┌───────────────┐
                                    │  SQL Server   │ ◄── Database
                                    └───────────────┘
```

---

## Key Architectural Principles (40k Feet)

* **Orchestration Layer:** LangGraph oversees the entire workflow, loops, and agent handoffs.
* **Worker & Decision Brain:** The Agent decides when to generate responses and when to invoke external capabilities.
* **Pluggable Capabilities:** LangChain/LLMs, RAG knowledge retrieval, and MCP tools connect cleanly under the agent.
* **Backend Isolation:** The LLM does not touch databases directly; it routes calls through trusted backend microservices (Node.js) to query SQL securely.
* **Core Mental Model:** Every box is just a standard function call or network request—any layer can be called directly whenever intermediate layers are not needed.


---

## Developer Translation: From Altitude to Code (Why It Looks the Way It Does)

* **Why it looks simple at 40k:** It hides all technical execution and infrastructure. It answers only *what business value is delivered*, not *how*.
* **Node.js Equivalent:** The high-level product feature definition (e.g., `POST /api/support-ticket` resolves customer issue).
