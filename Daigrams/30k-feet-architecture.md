# 30,000 Feet Architecture: Component & Integration View

```
                  [ User Request ]
                         │
                         ▼
┌─────────────────────────────────────────────────┐
│                    LangGraph                    │ ◄── Orchestrator (State, Loops)
│                                                 │
│       ┌─────────────────────────────────┐       │
│       │              AGENT              │       │
│       │  ┌───────────────────────────┐  │       │
│       │  │    LangChain + LLM        │  │       │ ◄── The Brain
│       │  │ (ChatOpenAI / Gemini / ...)│ │       │
│       │  └─────────────┬─────────────┘  │       │
│       └────────────────┼────────────────┘       │
└────────────────────────┼────────────────────────┘
                         │
            Agent decides which tool to call
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
┌───────────────┐                 ┌───────────────┐
│   RAG Tool    │                 │   MCP Tool    │ ◄── Tool Plug
│ (Vector DB)   │                 └───────┬───────┘
└───────────────┘                         │ HTTP / stdio
                                          ▼
                                  ┌───────────────┐
                                  │    Node.js    │ ◄── Your Backend Service
                                  └───────┬───────┘
                                          │ SQL
                                          ▼
                                  ┌───────────────┐
                                  │  SQL Server   │ ◄── Database
                                  └───────────────┘
```

---

## Key Architectural Principles (30k Feet)

* **Orchestrator Encapsulation:** LangGraph manages the state machine, cycles, and transitions, hosting the Agent within its graph nodes.
* **Autonomous Decision Brain:** The Agent inspects user state and decides whether to consult tools or produce an answer.
* **Unified Tool Abstraction:** Both RAG (vector retrieval) and MCP (external protocols) are exposed as standard tools to the agent.
* **Enterprise Boundary Protection:** The LLM never writes to SQL directly; it calls existing backend microservices (Node.js) which enforce authentication, business rules, and safe data access.
* **Core Mental Model:** Every box is ultimately a standard function call or network request that can be invoked directly if intermediate layers are not needed.


---

## Developer Translation: From Altitude to Code (Why It Looks the Way It Does)

* **Why it looks clean at 30k:** It shows component boundaries and responsibilities without revealing internal control flow or runtime infrastructure.
* **Comparison to 40k:** 40k shows only business outcome; 30k reveals the actual tech components (`LangGraph`, `Agent`, `MCP`, `Node.js`, `SQL`).
* **Node.js Equivalent:** The module architecture / package dependency diagram (e.g., `controller -> service -> repository`).
