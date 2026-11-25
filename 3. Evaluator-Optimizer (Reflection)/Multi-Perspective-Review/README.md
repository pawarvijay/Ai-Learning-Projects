# Multi-Perspective-Review vs Parallel-Voting

## Differences from `Parallel-Voting`
While `Parallel-Voting` asks multiple LLMs to answer the *same question* and picks a winner, `Multi-Perspective-Review` assigns **specialized critique personas** (Security vs Performance) that evaluate the *same artifact* and merge their critiques.

### 1. Dual Specialized Evaluation
```python
workflow.add_edge(START, "security")
workflow.add_edge(START, "performance")
```

### 2. Synthesis Consolidation
Instead of choosing one winner, the synthesizer ingests both critique domains to form a consolidated recommendation:
```python
workflow.add_edge("security", "synthesizer")
workflow.add_edge("performance", "synthesizer")
```
