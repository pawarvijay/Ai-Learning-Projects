# Architecture: Plan-and-Execute

```
[ Complex User Goal ]
          │
          ▼
┌──────────────────┐
│    LangGraph     │ StateGraph(PlanExecuteState)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    LangChain     │ Planner LLM + Worker LLM
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Plan & Execution │ Planner (Creates Task List) -> Worker Loop (Runs Task 1..N) -> Synthesizer
└──────────────────┘
```

```mermaid
graph TD
    START --> planner[Planner Agent]
    planner --> worker[Worker Agent]
    worker -->|has remaining subtasks| worker
    worker -->|all subtasks done| synth[Synthesizer / Aggregator]
    synth --> END
```
