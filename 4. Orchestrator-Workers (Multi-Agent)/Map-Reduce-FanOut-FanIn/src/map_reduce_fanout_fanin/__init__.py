import os
from typing import TypedDict, List
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


class MapReduceState(TypedDict):
    documents: List[str]
    chunk_1_summary: str
    chunk_2_summary: str
    final_synthesis: str


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
            max_output_tokens=30
        )
        for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


llm = get_model()


def map_worker_1(state: MapReduceState) -> dict:
    doc = state["documents"][0]
    print(f"\n[Map Worker 1]: Processing Chunk 1...")
    prompt = f"In under 8 words, summarize: {doc}"
    res = llm.invoke(prompt)
    s = getattr(res, "text", res.content).strip()
    print(f"  Summary 1: {s}")
    return {"chunk_1_summary": s}


def map_worker_2(state: MapReduceState) -> dict:
    doc = state["documents"][1]
    print(f"[Map Worker 2]: Processing Chunk 2...")
    prompt = f"In under 8 words, summarize: {doc}"
    res = llm.invoke(prompt)
    s = getattr(res, "text", res.content).strip()
    print(f"  Summary 2: {s}")
    return {"chunk_2_summary": s}


def reduce_worker(state: MapReduceState) -> dict:
    print(f"\n[Reduce Worker]: Merging all mapped chunk summaries...")
    combined = f"{state['chunk_1_summary']} + {state['chunk_2_summary']}"
    prompt = f"In under 12 words, synthesize these two points into one master takeaway: {combined}"
    res = llm.invoke(prompt)
    synthesis = getattr(res, "text", res.content).strip()
    print(f"  Final Synthesis: {synthesis}\n")
    return {"final_synthesis": synthesis}


def build_map_reduce_workflow():
    workflow = StateGraph(MapReduceState)
    workflow.add_node("map_1", map_worker_1)
    workflow.add_node("map_2", map_worker_2)
    workflow.add_node("reduce", reduce_worker)

    # Fan-Out to parallel map workers
    workflow.add_edge(START, "map_1")
    workflow.add_edge(START, "map_2")

    # Fan-In into reduce synthesizer
    workflow.add_edge("map_1", "reduce")
    workflow.add_edge("map_2", "reduce")
    workflow.add_edge("reduce", END)

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: 4. ORCHESTRATOR-WORKERS (MAP-REDUCE-FANOUT-FANIN)")
    print(" Flow: START -> [Map 1 | Map 2] (Parallel) -> Reduce -> END")
    print("=" * 65)

    app = build_map_reduce_workflow()
    docs = [
        "Chunk 1: LangGraph enables stateful cyclic agent graph execution.",
        "Chunk 2: Model Context Protocol standardizes tool execution across clouds."
    ]

    res = app.invoke({"documents": docs})
    print("=" * 65)
    print(f"Final Report: {res['final_synthesis']}")
    print("=" * 65)


if __name__ == "__main__":
    main()
