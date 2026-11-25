# 10,000 Feet Architecture: Graph Topology & State Machine

```
                                  START
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │         input_guard         │
                     │  - Validate user input      │
                     │  - Check session / tokens   │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │         intent_router       │
                     │  - Classify user request    │
                     └──────────────┬──────────────┘
                                    │
                 ┌──────────────────┴──────────────────┐
                 │ Conditional Edge: route_intent()    │
                 ▼                                     ▼
   [ "simple_query" ]                           [ "action_request" ]
         │                                             │
         ▼                                             ▼
┌─────────────────┐                             ┌─────────────────┐
│   direct_rag    │                             │   agent_reason  │◄────────┐
│ - Fetch Vector  │                             │ - Call LLM with │         │
│ - 1-Shot Answer │                             │   tool bindings │         │
└────────┬────────┘                             └────────┬────────┘         │
         │                                               │                  │
         │                                  ┌────────────┴────────────┐     │
         │                                  │  `should_continue()`    │     │
         │                                  ▼                         ▼     │
         │                         [ has tool_calls ]          [ no tools ] │
         │                                  │                         │     │
         │                                  ▼                         │     │
         │                       ┌─────────────────────┐              │     │
         │                       │    HITL Gate        │              │     │
         │                       │ (interrupt_before)  │              │     │
         │                       └──────────┬──────────┘              │     │
         │                                  │ Approved                │     │
         │                                  ▼                         │     │
         │                       ┌─────────────────────┐              │     │
         │                       │     tool_node       │              │     │
         │                       │ - Run MCP Tool      │              │     │
         │                       │ - Call Node.js API  │──────────────┘     │
         │                       └─────────────────────┘      (Loop back)   │
         │                                                            │     │
         └──────────────────────────────┬─────────────────────────────┘     │
                                        │                                   │
                                        ▼                                   │
                         ┌─────────────────────────────┐                    │
                         │       evaluator_node        │                    │
                         │ - Validate answer quality   │                    │
                         └──────────────┬──────────────┘                    │
                                        │                                   │
                         ┌──────────────┴──────────────┐                    │
                         │ Conditional: is_valid()     │                    │
                         ▼                             ▼                    │
                   [ Fail < 3 ]                   [ Pass / Final ]          │
                         │                             │                    │
                         └─────────────────────────────┼────────────────────┘
                                                       │
                                                       ▼
                                                      END
```

---

## Key State Machine Mechanics (10k Feet)

* **Explicit Nodes:** Each box is an isolated Python/TS function receiving `state: TypedDict` and returning partial state updates.
* **Deterministic Routing:** Conditional edges (`route_intent`, `should_continue`, `is_valid`) guide the flow based on data, not randomness.
* **Controlled Cycles:** The tool loop cycles back from `tool_node` $\rightarrow$ `agent_reason` until the agent decides to stop.
* **Human-in-the-Loop Interruption:** Sensitive tools pause execution before `tool_node` until human approval is delivered via the checkpointer.
* **Evaluator Guard:** Output is graded before hitting `END`, enabling self-correction if quality thresholds fail.


---

## Developer Translation: From Altitude to Code (Why It Looks Difficult)

* **Why it looks difficult at 10k:** It stops hand-waving and shows the actual branches, `if/else` checks, error conditions, and `while` loops of the state machine.
* **Comparison to 20k/30k:** 20k/30k draws one neat line (`Agent -> Tool`); 10k exposes the truth: *when to call, how to loop, when to stop, where to pause for human approval, and when to retry on failure*.
* **Node.js Equivalent:** The actual `async/await` business logic function:

```javascript
// The entire 10k diagram in plain JavaScript:
let state = { input, messages: [], attempts: 0 };

if (isSimpleQuery(state)) {
  return await directRag(state); // simple_query branch
}

// ReAct loop (agent_reason -> tool_node -> repeat)
while (true) {
  const decision = await callLLMWithTools(state);
  if (!decision.hasToolCalls) break; // should_continue -> no tools

  if (decision.tool.isSensitive) {
    await waitForHumanApproval();   // HITL Gate
  }

  const result = await executeTool(decision.tool);
  state.messages.push(result);      // Loop back!
}

return await evaluateAndReturn(state); // evaluator -> END
```
