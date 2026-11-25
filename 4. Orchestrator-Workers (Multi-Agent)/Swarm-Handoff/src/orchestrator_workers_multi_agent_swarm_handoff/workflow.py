import os
from typing import TypedDict, Literal
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


class SwarmState(TypedDict):
    customer_message: str
    active_agent: str
    agent_history: list[str]


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


def triage_agent(state: SwarmState) -> dict:
    print("\n[Triage Agent]: Answering user and evaluating handoff...")
    history = state.get("agent_history", []) + ["Triage Agent received user message"]
    if "refund" in state["customer_message"].lower():
        next_agent = "refund_agent"
        print("  -> Triage Agent performing HANDOFF to Refund Agent!")
    else:
        next_agent = "finish"
        print("  -> Triage Agent resolving request directly.")
    return {"active_agent": next_agent, "agent_history": history}


def refund_agent(state: SwarmState) -> dict:
    print("\n[Refund Agent]: Picked up handoff from Triage Agent!")
    prompt = f"In under 10 words, issue refund policy for: {state['customer_message']}"
    res = llm.invoke(prompt)
    ans = getattr(res, "text", res.content).strip()
    history = state.get("agent_history", []) + [f"Refund Agent: {ans}"]
    print(f"  Refund Action: {ans}")
    return {"active_agent": "finish", "agent_history": history}


def route_handoff(state: SwarmState) -> Literal["refund_agent", "__end__"]:
    if state["active_agent"] == "refund_agent":
        return "refund_agent"
    return END


def build_swarm_workflow():
    workflow = StateGraph(SwarmState)
    workflow.add_node("triage", triage_agent)
    workflow.add_node("refund_agent", refund_agent)

    workflow.add_edge(START, "triage")
    # Peer handoff: triage hands off directly to refund_agent
    workflow.add_conditional_edges("triage", route_handoff, {
        "refund_agent": "refund_agent",
        END: END
    })
    workflow.add_edge("refund_agent", END)

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: 4. ORCHESTRATOR-WORKERS (SWARM-HANDOFF)")
    print(" Flow: Triage Agent --(Peer Handoff)--> Refund Specialist Agent -> END")
    print("=" * 65)

    app = build_swarm_workflow()
    msg = "I was charged twice and want a refund immediately."
    print(f"User Message: \"{msg}\"")

    res = app.invoke({"customer_message": msg, "agent_history": []})
    print("\n" + "=" * 65)
    print("Handoff Audit Trail:")
    for h in res["agent_history"]:
        print(f"  • {h}")
    print("=" * 65)


if __name__ == "__main__":
    main()
