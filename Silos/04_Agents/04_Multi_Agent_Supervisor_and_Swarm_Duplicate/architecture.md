# Architecture: Supervisor-Router

```
[ User Ticket / Task ]
          │
          ▼
┌──────────────────┐
│    LangGraph     │ StateGraph(SupervisorState)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    LangChain     │ Supervisor Manager + Specialized Workers
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Manager Cycle   │ Supervisor <───► [ Coder Agent | Researcher Agent ]
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Finished / Exit  │ Supervisor routes to END when all worker outputs satisfactory
└──────────────────┘
```

```mermaid
graph TD
    START --> supervisor[Supervisor Agent Manager]
    supervisor -->|delegate coding| coder[Coder Worker Agent]
    supervisor -->|delegate research| researcher[Researcher Worker Agent]
    coder --> supervisor
    researcher --> supervisor
    supervisor -->|ticket resolved| END
```
