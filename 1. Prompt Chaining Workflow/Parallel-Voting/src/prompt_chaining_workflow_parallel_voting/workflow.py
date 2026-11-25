import os
from pathlib import Path
from typing import TypedDict
from dotenv import load_dotenv, find_dotenv

# Load API key
load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


# 1. State: Holds responses from 3 parallel models, plus the judge's pick
class VotingState(TypedDict):
    question: str
    creative_answer: str
    concise_answer: str
    technical_answer: str
    best_answer: str


# 2. Model with strict max 25 tokens (<10 words)
def get_model(temperature: float = 0.7):
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
            max_output_tokens=25  # Strict token saver
        ) for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


# 3. Parallel Worker Nodes (Running independently)
def creative_perspective(state: VotingState) -> dict:
    llm = get_model(temperature=0.9)
    prompt = f"In under 10 words, give a creative answer: {state['question']}"
    res = llm.invoke(prompt)
    ans = getattr(res, "text", res.content).strip()
    print(f"  [Creative Node]:  {ans}")
    return {"creative_answer": ans}


def concise_perspective(state: VotingState) -> dict:
    llm = get_model(temperature=0.1)
    prompt = f"In under 5 words, give the most direct answer: {state['question']}"
    res = llm.invoke(prompt)
    ans = getattr(res, "text", res.content).strip()
    print(f"  [Concise Node]:   {ans}")
    return {"concise_answer": ans}


def technical_perspective(state: VotingState) -> dict:
    llm = get_model(temperature=0.3)
    prompt = f"In under 10 words, give a technical answer: {state['question']}"
    res = llm.invoke(prompt)
    ans = getattr(res, "text", res.content).strip()
    print(f"  [Technical Node]: {ans}")
    return {"technical_answer": ans}


# 4. Aggregator / Judge Node (Fan-In: evaluates all 3 parallel results)
def judge_aggregator(state: VotingState) -> dict:
    print("\n[Judge Node]: Evaluating all 3 parallel answers...")
    llm = get_model(temperature=0.0)
    prompt = (
        f"Question: {state['question']}\n"
        f"Option A: {state['creative_answer']}\n"
        f"Option B: {state['concise_answer']}\n"
        f"Option C: {state['technical_answer']}\n"
        "In under 10 words, pick the best option and explain why:"
    )
    res = llm.invoke(prompt)
    verdict = getattr(res, "text", res.content).strip()
    print(f"\nWinner / Verdict:\n{verdict}\n")
    return {"best_answer": verdict}


# 5. Build Graph: Demonstrating Fan-Out (Parallel) -> Fan-In (Aggregation)
def build_parallel_voting_workflow():
    workflow = StateGraph(VotingState)

    # Register Nodes
    workflow.add_node("creative", creative_perspective)
    workflow.add_node("concise", concise_perspective)
    workflow.add_node("technical", technical_perspective)
    workflow.add_node("judge", judge_aggregator)

    # =========================================================================
    # THE KEY PARALLEL WIRING (Different from Linear-Sequential!):
    #
    # FAN-OUT: START connects to all 3 nodes simultaneously!
    # LangGraph runs creative, concise, and technical in parallel!
    # =========================================================================
    workflow.add_edge(START, "creative")
    workflow.add_edge(START, "concise")
    workflow.add_edge(START, "technical")

    # =========================================================================
    # FAN-IN: All 3 nodes must finish and funnel into the judge node!
    # =========================================================================
    workflow.add_edge("creative", "judge")
    workflow.add_edge("concise", "judge")
    workflow.add_edge("technical", "judge")

    # Finish at END
    workflow.add_edge("judge", END)

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: PROMPT CHAINING (PARALLEL-VOTING)")
    print(" Flow: START -> [Creative, Concise, Technical] (Parallel) -> Judge -> END")
    print("=" * 65)

    app = build_parallel_voting_workflow()

    initial_state = {"question": "What is the primary benefit of AI Agents?"}
    print(f"Question: \"{initial_state['question']}\"\n")
    print("Running 3 parallel evaluations...")
    app.invoke(initial_state)

    print("=" * 65)
    print(" Parallel-Voting Workflow Completed Successfully!")
    print("=" * 65)


if __name__ == "__main__":
    main()
