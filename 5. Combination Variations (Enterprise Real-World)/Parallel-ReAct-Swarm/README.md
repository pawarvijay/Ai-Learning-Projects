# Parallel-ReAct-Swarm vs Parallel-Voting

## Differences from `Parallel-Voting`
In `Parallel-Voting`, parallel nodes are simple prompts with different temperatures.

In **Parallel-ReAct-Swarm**, each parallel node is an **independent autonomous agent with its own dedicated tools** (e.g., News Search Agent vs. Financial API Agent). They run concurrently and feed their tool findings into an Executive Aggregator.

```python
# Fan-Out across distinct specialized tool agents
workflow.add_edge(START, "news_agent")
workflow.add_edge(START, "finance_agent")

# Fan-In into Aggregator
workflow.add_edge("news_agent", "aggregator")
workflow.add_edge("finance_agent", "aggregator")
```
