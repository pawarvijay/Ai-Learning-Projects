# Architecture: Dynamic-Memory-ReAct

```
[ User Request + Thread ID ]
              │
              ▼
┌──────────────────────────┐
│        LangGraph         │ StateGraph + MemorySaver Checkpointer
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│        LangChain         │ ChatGoogleGenerativeAI (tool calling)
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│     Multi-Turn Loop      │ Reads past thread checkpoints -> Invokes -> Saves new state
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│          Tools           │ lookup_weather
└──────────────────────────┘
```

```mermaid
graph TD
    START --> agent[Agent Brain LLM]
    agent -->|needs tool| tools[ToolNode Execution]
    tools --> agent
    agent -->|answer ready| checkpoint[(Checkpointer: Save Thread State)]
    checkpoint --> END
```
