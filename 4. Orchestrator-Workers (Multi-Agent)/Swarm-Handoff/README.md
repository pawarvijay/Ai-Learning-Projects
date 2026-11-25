# Swarm-Handoff vs Supervisor-Router

## Differences from `Supervisor-Router`
In `Supervisor-Router`, all communications flow through a **central boss/manager**. 

In **Swarm-Handoff**, there is no central manager. Agents communicate **peer-to-peer**:
* Agent A greets user.
* When Agent A detects specialized intent, it explicitly transfers control (hands off) to Agent B.
* Agent B takes over the conversation context directly.

```python
# Triage Agent hands off directly to Refund Agent:
workflow.add_conditional_edges("triage", route_handoff, {
    "refund_agent": "refund_agent",
    END: END
})
```
