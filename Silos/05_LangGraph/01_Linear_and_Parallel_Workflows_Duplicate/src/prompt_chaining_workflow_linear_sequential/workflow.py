import os
from pathlib import Path
from typing import TypedDict
from dotenv import load_dotenv, find_dotenv

# Load API key searching current working directory or package root
load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


# 1. Define State (Data flowing through the chain)
class ChainState(TypedDict):
    topic: str
    outline: str
    draft: str
    final_summary: str


# 2. Initialize Gemini Model with strict token limit (Max 10 tokens ~ 5-7 words)
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
            max_output_tokens=10  # Strict cap: guarantees short responses!
        ) for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


llm = get_model()


# 3. Define Nodes with strict short instructions (<10 words)
def generate_outline(state: ChainState) -> dict:
    print("\n[Step 1/3] Outline...")
    prompt = f"In under 10 words, give a 2-point outline for: {state['topic']}"
    response = llm.invoke(prompt)
    text = getattr(response, "text", response.content)
    print(f"{text}\n")
    return {"outline": text}


def write_draft(state: ChainState) -> dict:
    print("[Step 2/3] Draft...")
    prompt = f"In under 10 words, write a one-sentence draft from this outline: {state['outline']}"
    response = llm.invoke(prompt)
    text = getattr(response, "text", response.content)
    print(f"{text}\n")
    return {"draft": text}


def polish_and_summarize(state: ChainState) -> dict:
    print("[Step 3/3] Takeaway...")
    prompt = f"In under 7 words, summarize: {state['draft']}"
    response = llm.invoke(prompt)
    text = getattr(response, "text", response.content)
    print(f"{text}\n")
    return {"final_summary": text}


# 4. Build Linear Sequential Workflow
def build_linear_workflow():
    workflow = StateGraph(ChainState)

    # Add Nodes
    workflow.add_node("outline", generate_outline)
    workflow.add_node("draft", write_draft)
    workflow.add_node("summarize", polish_and_summarize)

    # Connect strictly in order: START -> outline -> draft -> summarize -> END
    workflow.add_edge(START, "outline")
    workflow.add_edge("outline", "draft")
    workflow.add_edge("draft", "summarize")
    workflow.add_edge("summarize", END)

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN 1: PROMPT CHAINING (LINEAR-SEQUENTIAL)")
    print(" Flow: START -> Outline -> Draft -> Summarize -> END")
    print("=" * 65)

    app = build_linear_workflow()

    initial_state = {"topic": "Model Context Protocol (MCP) in 2026"}
    app.invoke(initial_state)

    print("=" * 65)
    print(" Execution Completed Successfully!")
    print("=" * 65)


if __name__ == "__main__":
    main()
