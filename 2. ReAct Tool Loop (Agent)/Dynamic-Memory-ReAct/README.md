# Dynamic-Memory-ReAct vs Single-Agent-ReAct

## Differences from `Single-Agent-ReAct`
Instead of forgetting conversation state between runs, uses thread checkpointing for multi-turn short-term conversational memory.

### 1. Checkpointer Integration
Compiled with `checkpointer=MemorySaver()` (or `SqliteSaver` / `PostgresSaver` in prod):
```python
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)
```

### 2. Thread Identification
Every invocation passes a thread config to separate user sessions:
```python
config = {"configurable": {"thread_id": "session-101"}}
app.invoke({"messages": [("user", "Hello!")]}, config=config)

# Subsequent turns automatically recall previous messages on that thread_id
app.invoke({"messages": [("user", "What did I just say?")]}, config=config)
```
