# Human-in-the-Loop-Gate vs Single-Agent-ReAct

## Differences from `Single-Agent-ReAct`
Adds safety gates that pause execution before destructive/sensitive tools run.

### 1. Checkpointer & Interrupt Registration
Requires a persistence checkpointer (`MemorySaver` or `SqliteSaver`) and `interrupt_before`:
```python
checkpointer = MemorySaver()
app = workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["tools"]  # Pauses execution right before tool runs!
)
```

### 2. State Inspection & Resumption
Execution halts and returns control to caller. Caller inspects pending tool call and resumes with `None`:
```python
# 1. Inspect paused state
snapshot = agent.get_state(config)
pending = snapshot.values["messages"][-1].tool_calls[0]

# 2. Resume execution after human approval
agent.invoke(None, config=config)
```
