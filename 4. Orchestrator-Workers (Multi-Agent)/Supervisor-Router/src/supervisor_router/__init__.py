import os
from typing import TypedDict, Literal
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


class SupervisorState(TypedDict):
    request: str
    next_worker: str
    coder_output: str
    researcher_output: str
    final_output: str


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


def supervisor_node(state: SupervisorState) -> dict:
    print("\n[Supervisor Manager]: Assessing ticket & delegating to worker...")
    if not state.get("coder_output") and "code" in state["request"].lower():
        next_w = "coder"
    elif not state.get("researcher_output") and "research" in state["request"].lower():
        next_w = "researcher"
    else:
        next_w = "finish"

    print(f"  Supervisor Decision: Route to [{next_w.upper()}]")
    return {"next_worker": next_w}


def coder_worker(state: SupervisorState) -> dict:
    print("  -> [Coder Agent]: Writing snippet...")
    prompt = f"In under 10 words, write code for: {state['request']}"
    res = llm.invoke(prompt)
    ans = getattr(res, "text", res.content).strip()
    return {"coder_output": ans, "final_output": f"[Code]: {ans}"}


def research_worker(state: SupervisorState) -> dict:
    print("  -> [Researcher Agent]: Searching knowledgebase...")
    prompt = f"In under 10 words, research: {state['request']}"
    res = llm.invoke(prompt)
    ans = getattr(res, "text", res.content).strip()
    return {"researcher_output": ans, "final_output": f"[Research]: {ans}"}


def route_supervisor(state: SupervisorState) -> Literal["coder", "researcher", "__end__"]:
    w = state["next_worker"]
    if w == "coder":
        return "coder"
    elif w == "researcher":
        return "researcher"
    return END


def build_supervisor_workflow():
    workflow = StateGraph(SupervisorState)
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("coder", coder_worker)
    workflow.add_node("researcher", research_worker)

    workflow.add_edge(START, "supervisor")
    workflow.add_conditional_edges("supervisor", route_supervisor, {
        "coder": "coder",
        "researcher": "researcher",
        END: END
    })
    # Workers report back to Supervisor for next instructions or termination
    workflow.add_edge("coder", "supervisor")
    workflow.add_edge("researcher", "supervisor")

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: 4. ORCHESTRATOR-WORKERS (SUPERVISOR-ROUTER)")
    print(" Flow: Supervisor <-> [Coder Worker | Researcher Worker] -> END")
    print("=" * 65)

    app = build_supervisor_workflow()
    ticket = "Write python code to reverse a list"
    print(f"User Ticket: {ticket}")

    res = app.invoke({"request": ticket})
    print("\n" + "=" * 65)
    print(f"Delivered Result: {res.get('final_output', 'Completed')}")
    print("=" * 65)


if __name__ == "__main__":
    main()
