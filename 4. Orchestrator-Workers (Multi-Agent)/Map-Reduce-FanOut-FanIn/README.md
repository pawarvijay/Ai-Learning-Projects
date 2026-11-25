# Map-Reduce-FanOut-FanIn vs Parallel-Voting

## Differences from `Parallel-Voting`
In `Parallel-Voting`, parallel nodes compete to answer the *same single question*, and a judge picks the winner.

In **Map-Reduce**, parallel workers each process a **different slice/chunk of data** (e.g. Page 1, Page 2 of a 100-page book), and the **Reduce** node aggregates and synthesizes all pieces into one consolidated master report.

```python
# Fan-Out chunks across workers
workflow.add_edge(START, "map_1")
workflow.add_edge(START, "map_2")

# Fan-In to combine all chunk summaries
workflow.add_edge("map_1", "reduce")
workflow.add_edge("map_2", "reduce")
```
