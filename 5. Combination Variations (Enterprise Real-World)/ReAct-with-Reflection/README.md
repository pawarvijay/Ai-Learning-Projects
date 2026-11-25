# ReAct-with-Reflection vs Single-Agent-ReAct

## Differences from `Single-Agent-ReAct`
In standard `Single-Agent-ReAct`, when the agent finishes calling tools, it exits immediately to `END`.

In **ReAct-with-Reflection**, the agent is prevented from returning to the user directly. Instead, `should_continue` routes to an **Evaluator / Reflection Node** that grades and fact-checks the agent's summary against the ground truth tool outputs to eliminate hallucinations:

```python
def should_continue(state: State):
    if state["messages"][-1].tool_calls:
        return "tools"
    # Never exit directly! Pass to Reflection Grader first:
    return "reflection_node"
```
