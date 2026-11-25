# Architecture: Unit-Test-Driven-Loop

```
[ Code Specification ]
          │
          ▼
┌──────────────────┐
│    LangGraph     │ StateGraph(CodeGenState)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    LangChain     │ Coder LLM (Generates executable functions)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Test Runner    │ Deterministic Sandbox / Pytest Exec (Fails? -> Feed stacktrace back)
└──────────────────┘
```

```mermaid
graph TD
    START --> coder[Coder LLM]
    coder --> test_runner[Deterministic Unit Test Runner]
    test_runner -->|tests fail: send error| coder
    test_runner -->|all tests pass| END
```
