# Architecture: Parallel-Voting

```
[ User Prompt ]
       │
       ▼
┌──────────────────┐
│    LangGraph     │ StateGraph(VotingState)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    LangChain     │ ChatGoogleGenerativeAI (parallel invoke)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Parallel Fan-Out │ [Creative | Concise | Technical] -> Judge
└──────────────────┘
```

```mermaid
graph TD
    START --> creative[Creative Perspective]
    START --> concise[Concise Perspective]
    START --> technical[Technical Perspective]
    creative --> judge[Judge Aggregator]
    concise --> judge
    technical --> judge
    judge --> END
```
