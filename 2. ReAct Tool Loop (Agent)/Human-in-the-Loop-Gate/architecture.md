# Architecture: Human-in-the-Loop-Gate

```
[ User Prompt ]
       │
       ▼
┌──────────────────┐
│    LangGraph     │ StateGraph + MemorySaver Checkpoint
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    LangChain     │ ChatGoogleGenerativeAI (tool calling)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    HITL Gate     │ Agent -> [ PAUSE: Human Approval Required ] -> Tools -> END
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Sensitive Tool  │ transfer_money (executed only after human OK)
└──────────────────┘
```

```mermaid
graph TD
    START --> agent[Agent Brain LLM]
    agent -->|proposes sensitive tool| gate{INTERRUPT GATE}
    gate -->|wait for human review| human[Human Approval]
    human -->|approved: resume| tools[ToolNode Execution]
    tools --> agent
    agent -->|finished| END
```
