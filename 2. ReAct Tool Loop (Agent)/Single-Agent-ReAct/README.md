# Single-Agent-ReAct vs Linear-Sequential

## Differences from `Linear-Sequential`
Unlike fixed Prompt Chaining, ReAct introduces an autonomous reasoning and tool execution loop.

### 1. State Definition
Uses `add_messages` reducer to accumulate chat and tool history instead of overwriting:
```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
```

### 2. Tools Binding & ToolNode
Model is bound to executable tools:
```python
model_with_tools = model.bind_tools(tools)
workflow.add_node("tools", ToolNode(tools))
```

### 3. Cyclic Loop Edge
Execution loops back from `tools` to `agent`:
```python
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")  # The ReAct cycle!
```
