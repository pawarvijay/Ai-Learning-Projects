# Routing-Classifier vs Linear-Sequential

## Differences from `Linear-Sequential`
Rest of the project setup is the same. The difference is replacing the linear pipeline with a **Classifier** node and a **Path-Map Conditional Edge**.

### 1. Classifier Router Function
```python
def route_decision(state: RoutingState) -> str:
    return state["category"]
```

### 2. Path Map Wiring
Instead of direct edges, routes dynamically to exactly one specialized node:
```python
workflow.add_conditional_edges(
    "classifier",
    route_decision,
    {
        "billing": "billing",
        "technical": "technical",
        "general": "general"
    }
)
```
