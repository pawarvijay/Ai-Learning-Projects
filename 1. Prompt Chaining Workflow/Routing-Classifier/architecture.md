# Architecture: Routing-Classifier

```
[ User Prompt ]
       │
       ▼
┌──────────────────┐
│    LangGraph     │ StateGraph(RoutingState)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    LangChain     │ ChatGoogleGenerativeAI (Classification)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Dynamic Branch  │ Classifier -> [Billing | Tech | General] -> END
└──────────────────┘
```

```mermaid
graph TD
    START --> classifier[Classifier Node]
    classifier -->|billing| billing[Billing Specialist]
    classifier -->|technical| tech[Tech Support]
    classifier -->|general| general[General Care]
    billing --> END
    tech --> END
    general --> END
```
