import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def transfer_money(amount: float, recipient: str) -> str:
    """Critical financial tool requiring human sign-off."""
    return f"SUCCESS: Transferred ${amount:.2f} to {recipient}."


tools = [transfer_money]


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
        ).bind_tools(tools)
        for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


model_with_tools = get_model()


def call_model(state: AgentState):
    return {"messages": [model_with_tools.invoke(state["messages"])]}


def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END


def build_hitl_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")

    checkpointer = MemorySaver()
    # Interrupt execution right before running the tools node
    return workflow.compile(checkpointer=checkpointer, interrupt_before=["tools"])


def main():
    print("=" * 65)
    print(" PATTERN: 2. REACT TOOL LOOP (HUMAN-IN-THE-LOOP-GATE)")
    print(" Flow: Agent proposes sensitive tool -> PAUSE -> Human OK -> Resume")
    print("=" * 65)

    agent = build_hitl_agent()
    config = {"configurable": {"thread_id": "transfer-session-101"}}

    query = "Transfer $5000 to Bob for consulting fee."
    print(f"User Request: {query}\n")

    # Step 1: Run until the gate interrupts execution
    print("[Phase 1]: Running until Human Approval Gate...")
    agent.invoke({"messages": [("user", query)]}, config=config)

    snapshot = agent.get_state(config)
    pending_tool = snapshot.values["messages"][-1].tool_calls[0]
    print(f"\n[!] EXECUTION PAUSED BY HITL GATE!")
    print(f"    Pending Tool Call : {pending_tool['name']}")
    print(f"    Arguments         : {pending_tool['args']}")

    # Step 2: Simulate human approval
    print("\n[Human]: Approving transaction...")

    # Step 3: Resume by invoking with None
    res = agent.invoke(None, config=config)
    print("\n[Phase 2]: Resumed & Completed:")
    for msg in res["messages"]:
        if msg.type == "tool":
            print(f"  Tool Executed: {msg.content}")
        elif msg.type == "ai" and msg.content:
            text = getattr(msg, "text", msg.content)
            print(f"  Final Confirmation: {text}")

    print("=" * 65)


if __name__ == "__main__":
    main()
