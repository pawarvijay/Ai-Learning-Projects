import os
from typing import TypedDict, List
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


class PlanExecuteState(TypedDict):
    goal: str
    plan: List[str]
    completed_steps: List[str]
    final_result: str


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
            max_output_tokens=35
        )
        for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


llm = get_model()


def planner_node(state: PlanExecuteState) -> dict:
    print(f"\n[Planner Agent]: Decomposing goal into steps...")
    # Creates 2 subtasks
    plan = [
        f"1. Research architecture for: {state['goal']}",
        f"2. Write implementation guide for: {state['goal']}"
    ]
    for step in plan:
        print(f"  • {step}")
    return {"plan": plan, "completed_steps": []}


def worker_node(state: PlanExecuteState) -> dict:
    step_idx = len(state.get("completed_steps", []))
    current_step = state["plan"][step_idx]
    print(f"\n[Worker Agent]: Executing Step {step_idx + 1} -> '{current_step}'")

    prompt = f"In under 10 words, execute this task: {current_step}"
    res = llm.invoke(prompt)
    output = getattr(res, "text", res.content).strip()
    print(f"  Step Output: {output}")

    completed = state.get("completed_steps", []) + [output]
    return {"completed_steps": completed}


def should_continue(state: PlanExecuteState) -> str:
    if len(state["completed_steps"]) >= len(state["plan"]):
        return "synthesizer"
    return "worker"


def synthesizer_node(state: PlanExecuteState) -> dict:
    print(f"\n[Synthesizer Node]: Aggregating worker execution results...")
    final = " | ".join(state["completed_steps"])
    return {"final_result": final}


def build_plan_execute_workflow():
    workflow = StateGraph(PlanExecuteState)
    workflow.add_node("planner", planner_node)
    workflow.add_node("worker", worker_node)
    workflow.add_node("synthesizer", synthesizer_node)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "worker")
    workflow.add_conditional_edges("worker", should_continue, {"worker": "worker", "synthesizer": "synthesizer"})
    workflow.add_edge("synthesizer", END)

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: 4. ORCHESTRATOR-WORKERS (PLAN-AND-EXECUTE)")
    print(" Flow: Planner -> Worker (loops over plan items) -> Synthesizer")
    print("=" * 65)

    app = build_plan_execute_workflow()
    goal = "Deploy Microservice on Kubernetes"
    print(f"Goal: {goal}")

    res = app.invoke({"goal": goal})
    print("\n" + "=" * 65)
    print(f"Final Aggregated Result:\n{res['final_result']}")
    print("=" * 65)


if __name__ == "__main__":
    main()
