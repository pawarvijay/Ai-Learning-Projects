# Chain-Wrapped-ReAct vs Single-Agent-ReAct

## Differences from `Single-Agent-ReAct`
In a pure ReAct agent, user input directly enters the LLM and raw tool output goes directly to the user.

In **Chain-Wrapped-ReAct**, deterministic security/guardrail steps wrap the agent:
1. **Input Guard Node:** Sanitizes and checks permissions before the LLM runs.
2. **ReAct Loop:** Autonomous tool execution cycle in the middle.
3. **Output Guard Node:** Scrubs sensitive data (PII, credit cards, SSN) before sending to user.

```python
workflow.add_edge(START, "input_guard")
workflow.add_edge("input_guard", "agent")          # Enters agent loop
# Agent loops with tools...
workflow.add_edge("output_guard", END)             # Exits through output scrubber
```
