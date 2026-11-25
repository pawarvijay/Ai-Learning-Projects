import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool


class EnterpriseState(TypedDict):
    ticket_id: str
    user_request: str
    category: str
    messages: Annotated[list, add_messages]
    qa_score: int
    approved: bool
    final_output: str


@tool
def deploy_hotfix(service: str) -> str:
    """Production deployment tool."""
    return f"DEPLOYED: Hotfix rolled out to cluster {service}."


tools = [deploy_hotfix]


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
        ).bind_tools(tools)
        for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


model_with_tools = get_model()


# Stage 1: Router
def intake_router(state: EnterpriseState) -> dict:
    print("\n[Stage 1: Enterprise Router]: Ingesting ticket...")
    return {"category": "devops_critical", "messages": [("user", state["user_request"])]}


# Stage 2: Specialist Worker Agent
def worker_agent(state: EnterpriseState) -> dict:
    print("[Stage 2: DevOps Worker Agent]: Analyzing deployment request...")
    return {"messages": [model_with_tools.invoke(state["messages"])]}


def should_continue_worker(state: EnterpriseState):
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tools"
    return "qa_evaluator"


# Stage 3: Evaluator Grader
def qa_evaluator(state: EnterpriseState) -> dict:
    print("[Stage 3: QA Evaluator Grader]: Inspecting deployment output...")
    return {"qa_score": 10}


# Stage 4: Human-in-the-Loop Sign-off
def final_signoff(state: EnterpriseState) -> dict:
    print("\n[Stage 4: Executive Sign-off]: Delivering verified release...")
    raw = state["messages"][-1].content
    raw_text = getattr(state["messages"][-1], "text", raw)
    return {"final_output": f"ENTERPRISE-VERIFIED: {raw_text}"}


def build_enterprise_pipeline():
    workflow = StateGraph(EnterpriseState)
    workflow.add_node("router", intake_router)
    workflow.add_node("worker", worker_agent)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_node("qa_evaluator", qa_evaluator)
    workflow.add_node("signoff", final_signoff)

    workflow.add_edge(START, "router")
    workflow.add_edge("router", "worker")

    workflow.add_conditional_edges("worker", should_continue_worker, {
        "tools": "tools",
        "qa_evaluator": "qa_evaluator"
    })
    workflow.add_edge("tools", "worker")
    workflow.add_edge("qa_evaluator", "signoff")
    workflow.add_edge("signoff", END)

    # Human Gate: pause right before sensitive tool execution
    return workflow.compile(checkpointer=MemorySaver(), interrupt_before=["tools"])


def main():
    print("=" * 65)
    print(" PATTERN: 5. COMBINATION (FULL-ENTERPRISE-PIPELINE)")
    print(" Flow: Router -> Worker ReAct Loop -> HITL Gate -> QA Grader -> Signoff")
    print("=" * 65)

    app = build_enterprise_pipeline()
    cfg = {"configurable": {"thread_id": "enterprise-release-900"}}

    req = "Deploy critical hotfix for payments-service immediately."
    print(f"Incoming Incident: {req}")

    # Phase 1: Executes until HITL gate
    print("\n[Phase 1: Running Automated Pipeline...]")
    app.invoke({"ticket_id": "INC-99", "user_request": req}, config=cfg)

    # Check paused state
    snapshot = app.get_state(cfg)
    pending = snapshot.values["messages"][-1].tool_calls[0]
    print(f"\n[!] HITL GATE TRIGGERED: Production release requires sign-off!")
    print(f"    Pending Action: {pending['name']}({pending['args']})")

    # Phase 2: Human approves
    print("\n[Lead Engineer]: Approved. Resuming pipeline...")
    res = app.invoke(None, config=cfg)

    print("\n[Phase 2: Completed Successfully]")
    print(f"Final Status: {res['final_output']}")
    print("=" * 65)


if __name__ == "__main__":
    main()
