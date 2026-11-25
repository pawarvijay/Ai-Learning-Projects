import os
from typing import TypedDict
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


class ReviewState(TypedDict):
    proposal: str
    security_critique: str
    perf_critique: str
    final_decision: str


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
            max_output_tokens=30
        )
        for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


llm = get_model()


def security_auditor(state: ReviewState) -> dict:
    prompt = f"In under 10 words, give a security critique of: {state['proposal']}"
    res = llm.invoke(prompt)
    critique = getattr(res, "text", res.content).strip()
    print(f"  [Security Auditor]: {critique}")
    return {"security_critique": critique}


def performance_auditor(state: ReviewState) -> dict:
    prompt = f"In under 10 words, give a performance critique of: {state['proposal']}"
    res = llm.invoke(prompt)
    critique = getattr(res, "text", res.content).strip()
    print(f"  [Performance Auditor]: {critique}")
    return {"perf_critique": critique}


def synthesizer_node(state: ReviewState) -> dict:
    prompt = (
        f"Proposal: {state['proposal']}\n"
        f"Security Feedback: {state['security_critique']}\n"
        f"Perf Feedback: {state['perf_critique']}\n"
        "In under 12 words, synthesize into a final engineering recommendation:"
    )
    res = llm.invoke(prompt)
    decision = getattr(res, "text", res.content).strip()
    print(f"\n[Final Synthesis]: {decision}\n")
    return {"final_decision": decision}


def build_review_workflow():
    workflow = StateGraph(ReviewState)
    workflow.add_node("security", security_auditor)
    workflow.add_node("performance", performance_auditor)
    workflow.add_node("synthesizer", synthesizer_node)

    # Parallel Fan-Out Review
    workflow.add_edge(START, "security")
    workflow.add_edge(START, "performance")

    # Fan-In into Synthesis
    workflow.add_edge("security", "synthesizer")
    workflow.add_edge("performance", "synthesizer")
    workflow.add_edge("synthesizer", END)

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: 3. EVALUATOR-OPTIMIZER (MULTI-PERSPECTIVE-REVIEW)")
    print(" Flow: Proposal -> Parallel [Security, Perf] Evaluators -> Synthesizer")
    print("=" * 65)

    app = build_review_workflow()
    proposal = "Store all user JWT tokens in browser localStorage without expiry."
    print(f"Proposal: {proposal}\n")

    res = app.invoke({"proposal": proposal})
    print("=" * 65)


if __name__ == "__main__":
    main()
