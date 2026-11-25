# Unit-Test-Driven-Loop vs Self-Correction-Loop

## Differences from `Self-Correction-Loop`
Instead of an LLM judging the output qualitatively (subjective review), a **deterministic compiler / test-runner node** executes unit tests against the generated artifact.

### 1. Deterministic Evaluation Node
The evaluator is pure Python test logic, not an LLM prompt:
```python
def test_runner_node(state: CodeGenState):
    # Runs actual pytest or assertions
    try:
        run_sandbox_tests(state["code"])
        return {"test_passed": True, "test_error": ""}
    except Exception as e:
        return {"test_passed": False, "test_error": str(e)}
```

### 2. Error-Driven Self-Healing
If assertions fail, the exact stack trace / error string is injected back into the generator for targeted healing.
