import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool


class HybridState(TypedDict):
    raw_input: str
    sanitized_input: str
    messages: Annotated[list, add_messages]
    pii_cleaned_output: str


@tool
def query_account_balance(account_id: str) -> str:
    """Returns confidential account balance."""
    return f"Account {account_id} balance is $14,250.00. SSN: 000-12-3456"


tools = [query_account_balance]


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


# Step 1: Sequential Input Guard Node
def input_guard_node(state: HybridState) -> dict:
    print("\n[Step 1: Input Guard]: Validating and sanitizing input query...")
    clean = state["raw_input"].strip()
    return {"sanitized_input": clean, "messages": [("user", clean)]}


# Step 2: Autonomous ReAct Agent Loop
def agent_brain_node(state: HybridState) -> dict:
    return {"messages": [model_with_tools.invoke(state["messages"])]}


def should_continue(state: HybridState):
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tools"
    return "output_guard"


# Step 3: Sequential Output PII Scrubber Node
def output_guard_node(state: HybridState) -> dict:
    print("\n[Step 3: Output Guard]: Scrubbing PII and formatting final response...")
    raw = state["messages"][-1].content
    raw_text = getattr(state["messages"][-1], "text", raw)
    # Scrub sensitive SSN numbers before showing to user
    scrubbed = str(raw_text).replace("000-12-3456", "[REDACTED-SSN]")
    return {"pii_cleaned_output": scrubbed}


def build_chain_wrapped_react():
    workflow = StateGraph(HybridState)

    # Register workflow & agent nodes
    workflow.add_node("input_guard", input_guard_node)
    workflow.add_node("agent", agent_brain_node)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_node("output_guard", output_guard_node)

    # 1. Linear edge into Agent
    workflow.add_edge(START, "input_guard")
    workflow.add_edge("input_guard", "agent")

    # 2. Autonomous ReAct Loop
    workflow.add_conditional_edges("agent", should_continue, {
        "tools": "tools",
        "output_guard": "output_guard"
    })
    workflow.add_edge("tools", "agent")

    # 3. Linear edge out of Agent through PII guard to END
    workflow.add_edge("output_guard", END)

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: 5. COMBINATION (CHAIN-WRAPPED-REACT)")
    print(" Flow: Input Guard (Chain) -> ReAct Agent Loop -> Output Guard (Chain)")
    print("=" * 65)

    app = build_chain_wrapped_react()
    query = "Check balance for account ACC-888"
    print(f"User Request: {query}")

    res = app.invoke({"raw_input": query})
    print("\n" + "=" * 65)
    print(f"Safe Delivered Response:\n{res['pii_cleaned_output']}")
    print("=" * 65)


if __name__ == "__main__":
    main()
