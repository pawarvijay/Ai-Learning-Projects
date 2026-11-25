# Supervisor-Router vs Routing-Classifier

## Differences from `Routing-Classifier`
In `Routing-Classifier`, the router branches to a leaf node that immediately exits to `END`. 

In **Supervisor-Router**, the Supervisor is an autonomous manager:
1. It delegates tasks to specialized worker agents (`coder`, `researcher`).
2. **Workers report BACK to the supervisor** (`workflow.add_edge("coder", "supervisor")`).
3. The supervisor inspects intermediate outputs and can delegate to another worker or finish.

```python
workflow.add_edge("coder", "supervisor")       # Reports back to manager!
workflow.add_edge("researcher", "supervisor")  # Reports back to manager!
```
