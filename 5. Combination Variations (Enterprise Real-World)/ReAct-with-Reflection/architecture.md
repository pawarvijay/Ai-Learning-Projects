# Architecture: ReAct-with-Reflection

```
[ User Query ]
       │
       ▼
┌──────────────────┐
│    LangGraph     │ StateGraph(State)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    LangChain     │ ChatGoogleGenerativeAI (tool calling + reflection)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    ReAct Loop    │ Agent Brain <───► ToolNode (Retrieval / Action)
└────────┬─────────┘
         │ (Tools finished)
         ▼
┌──────────────────┐
│ Reflection Node  │ Fact-Checker / Hallucination Grader ──► Verified Answer ──► END
└──────────────────┘
```

```mermaid
graph TD
    START --> agent[ReAct Agent Brain]
    agent -->|needs tool| tools[ToolNode Execution]
    tools --> agent
    agent -->|answer formulated| reflect[Reflection Fact-Checker Grader]
    reflect -->|verified ground truth| END
```
