# Architecture: Multi-Perspective-Review

```
[ System Proposal ]
        │
        ▼
┌──────────────────┐
│    LangGraph     │ StateGraph(ReviewState)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    LangChain     │ Security Auditor + Performance Auditor
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Parallel Review  │ [ Security Critique | Perf Critique ] -> Synthesizer -> END
└──────────────────┘
```

```mermaid
graph TD
    START --> security[Security Reviewer]
    START --> perf[Performance Reviewer]
    security --> synth[Engineering Synthesizer]
    perf --> synth
    synth --> END
```
