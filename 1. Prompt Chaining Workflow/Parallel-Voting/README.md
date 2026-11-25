# Parallel-Voting vs Linear-Sequential

## Differences from `Linear-Sequential`
All prompt loading, `.env`, and model initialization logic are identical. The differences are strictly in State and graph wiring:

### 1. State Differences
`Linear-Sequential` passes one draft downstream. `Parallel-Voting` stores 3 candidate outputs:
```python
class VotingState(TypedDict):
    question: str
    creative_answer: str
    concise_answer: str
    technical_answer: str
    best_answer: str
```

### 2. Fan-Out & Fan-In Graph Wiring
Instead of `START -> outline -> draft`:
```python
# Fan-Out
workflow.add_edge(START, "creative")
workflow.add_edge(START, "concise")
workflow.add_edge(START, "technical")

# Fan-In to Aggregator Judge
workflow.add_edge("creative", "judge")
workflow.add_edge("concise", "judge")
workflow.add_edge("technical", "judge")
workflow.add_edge("judge", END)
```
