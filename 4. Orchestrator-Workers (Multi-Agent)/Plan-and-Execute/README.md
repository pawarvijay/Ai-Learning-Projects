# Plan-and-Execute vs ReAct

## Differences from `ReAct`
Instead of deciding the next step dynamically on every turn (ReAct), the **Planner** creates a full sequence of subtasks upfront, and **Worker** nodes iteratively execute each planned step until all are complete.

### 1. Plan State Management
Maintains a list of future plan tasks and completed task outputs:
```python
class PlanExecuteState(TypedDict):
    goal: str
    plan: List[str]
    completed_steps: List[str]
    final_result: str
```

### 2. Task Progression Loop
Loops over the plan items until `len(completed_steps) == len(plan)`:
```python
def should_continue(state: PlanExecuteState):
    if len(state["completed_steps"]) >= len(state["plan"]):
        return "synthesizer"
    return "worker"
```
