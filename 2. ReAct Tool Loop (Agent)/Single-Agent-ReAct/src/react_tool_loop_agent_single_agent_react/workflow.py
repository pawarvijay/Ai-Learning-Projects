import os
from pathlib import Path
from typing import TypedDict, Annotated
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def calculate_discount(price: float, discount_pct: float) -> str:
    """Calculates discounted price given price and discount percentage."""
    final_price = price * (1 - discount_pct / 100)
    return f"Final discounted price is ${final_price:.2f}"


tools = [calculate_discount]


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


def call_model(state: AgentState):
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END


def build_react_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")
    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: 2. REACT TOOL LOOP (SINGLE-AGENT)")
    print(" Flow: START -> Agent <-> ToolNode -> END")
    print("=" * 65)

    agent = build_react_agent()
    query = "Calculate a 20% discount on a $250 item."
    print(f"User Query: {query}\n")

    res = agent.invoke({"messages": [("user", query)]})
    for msg in res["messages"]:
        if getattr(msg, "tool_calls", None):
            print(f"[Tool Call]: {msg.tool_calls[0]['name']} -> {msg.tool_calls[0]['args']}")
        elif msg.type == "tool":
            print(f"[Tool Result]: {msg.content}")
        elif msg.type == "ai" and msg.content:
            text = getattr(msg, "text", msg.content)
            print(f"[Agent Response]: {text}")

    print("=" * 65)


if __name__ == "__main__":
    main()
