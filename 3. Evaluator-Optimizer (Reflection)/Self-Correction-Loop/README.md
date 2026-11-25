# Self-Correction-Loop vs Linear-Sequential

## Differences from `Linear-Sequential`
Unlike single-pass generation, the Evaluator-Optimizer pattern uses an evaluation feedback loop that grades output and forces self-correction.

### 1. State Tracking
Tracks critique, score, and loop iteration counts:
```python
class ReflectionState(TypedDict):
    task: str
    draft: str
    critique: str
    score: int
    iterations: int
```

### 2. Quality Evaluation Conditional Edge
Instead of flowing directly to `END`, checks whether quality criteria are met:
```python
def should_loop(state: ReflectionState):
    if state["score"] >= 8 or state["iterations"] >= 3:
        return END
    return "generate"  # Loops back to generator with critique!

workflow.add_conditional_edges("evaluate", should_loop)
```
