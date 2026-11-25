import os
from typing import TypedDict, Literal
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


class CodeGenState(TypedDict):
    specification: str
    code: str
    test_passed: bool
    test_error: str
    iterations: int


def get_model():
    candidates = [
        os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        "gemini-3.1-flash-lite",
        "gemini-3.6-flash",
        "gemini-3.7-flash",
        "gemini-3.5-flash"
    ]
    models = [
        ChatGoogleGenerativeAI(
            model=m,
            temperature=0,
            timeout=20,
            max_retries=0,
            max_output_tokens=60
        )
        for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


llm = get_model()


def coder_node(state: CodeGenState) -> dict:
    iter_count = state.get("iterations", 0) + 1
    print(f"\n[Coder Node (Iter {iter_count})]: Generating Python function...")

    if not state.get("test_error"):
        prompt = f"Write ONLY a Python function: {state['specification']}. Do not explain."
    else:
        prompt = f"Fix this code:\n{state['code']}\nError: {state['test_error']}. Return ONLY valid python function:"

    res = llm.invoke(prompt)
    code = getattr(res, "text", res.content).strip()
    print(f"  Generated code length: {len(code)} chars")
    return {"code": code, "iterations": iter_count}


def test_runner_node(state: CodeGenState) -> dict:
    print(f"[Test Runner Node]: Executing deterministic unit tests...")
    # Simulated execution check (passes on iteration 2)
    if state["iterations"] == 1:
        passed = False
        error = "AssertionError: calculate_tax(100) expected 115 but got 110"
    else:
        passed = True
        error = ""

    print(f"  Test Result: {'PASSED (OK)' if passed else 'FAILED: ' + error}")
    return {"test_passed": passed, "test_error": error}


def should_continue(state: CodeGenState) -> Literal["coder", "__end__"]:
    if state["test_passed"] or state["iterations"] >= 3:
        return END
    return "coder"


def build_unit_test_workflow():
    workflow = StateGraph(CodeGenState)
    workflow.add_node("coder", coder_node)
    workflow.add_node("test_runner", test_runner_node)

    workflow.add_edge(START, "coder")
    workflow.add_edge("coder", "test_runner")
    workflow.add_conditional_edges("test_runner", should_continue, {"coder": "coder", END: END})

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: 3. EVALUATOR-OPTIMIZER (UNIT-TEST-DRIVEN-LOOP)")
    print(" Flow: Coder -> Deterministic Unit Tests -> Self-heal on failure")
    print("=" * 65)

    app = build_unit_test_workflow()
    spec = "def calculate_tax(amount: float) -> float: adds 15% tax"
    res = app.invoke({"specification": spec, "iterations": 0})

    print("\n" + "=" * 65)
    print(f"Tests Passed: {res['test_passed']}")
    print(f"Total Iterations: {res['iterations']}")
    print("=" * 65)


if __name__ == "__main__":
    main()
