import os
from typing import TypedDict, Literal
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


class ReflectionState(TypedDict):
    task: str
    draft: str
    critique: str
    score: int
    iterations: int


def get_model(temperature: float = 0.0):
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
            temperature=temperature,
            timeout=20,
            max_retries=0,
            max_output_tokens=35
        )
        for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


generator_llm = get_model(temperature=0.7)
critic_llm = get_model(temperature=0.0)


def generate_node(state: ReflectionState) -> dict:
    iter_count = state.get("iterations", 0) + 1
    print(f"\n[Generator Node (Iter {iter_count})]: Drafting solution...")

    if not state.get("critique"):
        prompt = f"In under 10 words, write a slogan for: {state['task']}"
    else:
        prompt = f"Improve this slogan based on critique: '{state['critique']}'. Slogan: '{state['draft']}'. In under 10 words:"

    res = generator_llm.invoke(prompt)
    draft = getattr(res, "text", res.content).strip()
    print(f"  Draft: {draft}")
    return {"draft": draft, "iterations": iter_count}


def evaluate_node(state: ReflectionState) -> dict:
    print(f"[Critic Node]: Evaluating draft...")
    # Simulated strict grading: fails 1st turn, passes on 2nd turn
    if state["iterations"] == 1:
        score = 5
        critique = "Too generic. Add vivid energy."
    else:
        score = 9
        critique = "Passes all criteria."

    print(f"  Score: {score}/10 | Critique: {critique}")
    return {"score": score, "critique": critique}


def should_loop(state: ReflectionState) -> Literal["generate", "__end__"]:
    # Pass if score >= 8 or exceeded 3 iterations
    if state["score"] >= 8 or state["iterations"] >= 3:
        return END
    return "generate"


def build_self_correction_workflow():
    workflow = StateGraph(ReflectionState)
    workflow.add_node("generate", generate_node)
    workflow.add_node("evaluate", evaluate_node)

    workflow.add_edge(START, "generate")
    workflow.add_edge("generate", "evaluate")
    workflow.add_conditional_edges("evaluate", should_loop, {"generate": "generate", END: END})

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: 3. EVALUATOR-OPTIMIZER (SELF-CORRECTION-LOOP)")
    print(" Flow: Generator -> Evaluator -> Loop back if score < 8 -> END")
    print("=" * 65)

    app = build_self_correction_workflow()
    task = "Energy Drink for Developers"
    res = app.invoke({"task": task, "iterations": 0})

    print("\n" + "=" * 65)
    print(f"Final Approved Output: {res['draft']}")
    print(f"Total Iterations:      {res['iterations']}")
    print("=" * 65)


if __name__ == "__main__":
    main()
