import os
from pathlib import Path
from typing import TypedDict, Literal
from dotenv import load_dotenv, find_dotenv

# Load API key
load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


# 1. State: Holds request, classification decision, and targeted response
class RoutingState(TypedDict):
    user_query: str
    category: Literal["billing", "technical", "general"]
    response: str


# 2. Model setup with strict token saver (<10 words)
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
            max_output_tokens=25  # Strict token saver
        ) for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


llm = get_model()


# 3. Step 1: The Classifier Node (Decides which path to take)
def classifier_node(state: RoutingState) -> dict:
    print(f"\n[Classifier Node]: Analyzing query -> '{state['user_query']}'")
    prompt = (
        "Classify this support request into EXACTLY one word: 'billing', 'technical', or 'general'.\n"
        f"Request: {state['user_query']}\n"
        "Classification:"
    )
    res = llm.invoke(prompt)
    raw_cat = getattr(res, "text", res.content).strip().lower()

    # Normalize category fallback
    if "billing" in raw_cat:
        category = "billing"
    elif "technical" in raw_cat:
        category = "technical"
    else:
        category = "general"

    print(f"Decision: Classified as [{category.upper()}]")
    return {"category": category}


# 4. Specialized Branch Nodes (Only ONE of these runs!)
def billing_specialist(state: RoutingState) -> dict:
    print("  -> Routed to [Billing Specialist Node]")
    prompt = f"In under 10 words, give a billing refund reply for: {state['user_query']}"
    res = llm.invoke(prompt)
    reply = getattr(res, "text", res.content).strip()
    return {"response": f"[Billing Dept]: {reply}"}


def technical_specialist(state: RoutingState) -> dict:
    print("  -> Routed to [Technical Support Node]")
    prompt = f"In under 10 words, give a technical troubleshooting reply for: {state['user_query']}"
    res = llm.invoke(prompt)
    reply = getattr(res, "text", res.content).strip()
    return {"response": f"[Tech Support]: {reply}"}


def general_specialist(state: RoutingState) -> dict:
    print("  -> Routed to [General Inquiry Node]")
    prompt = f"In under 10 words, answer this general customer question: {state['user_query']}"
    res = llm.invoke(prompt)
    reply = getattr(res, "text", res.content).strip()
    return {"response": f"[Customer Care]: {reply}"}


# 5. Conditional Router Function (The Traffic Police)
def route_decision(state: RoutingState) -> str:
    # Looks at what classifier_node returned and routes directly to that node!
    return state["category"]


# 6. Build Graph: Demonstrating Dynamic Branching via Conditional Edges
def build_routing_workflow():
    workflow = StateGraph(RoutingState)

    # Add Nodes
    workflow.add_node("classifier", classifier_node)
    workflow.add_node("billing", billing_specialist)
    workflow.add_node("technical", technical_specialist)
    workflow.add_node("general", general_specialist)

    # START goes into classifier
    workflow.add_edge(START, "classifier")

    # =========================================================================
    # THE KEY ROUTING WIRING (Different from Linear & Parallel!):
    #
    # The classifier dynamically routes to ONLY ONE node based on category!
    # =========================================================================
    workflow.add_conditional_edges(
        "classifier",
        route_decision,
        {
            "billing": "billing",
            "technical": "technical",
            "general": "general"
        }
    )

    # All specialized branches lead straight to END
    workflow.add_edge("billing", END)
    workflow.add_edge("technical", END)
    workflow.add_edge("general", END)

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: PROMPT CHAINING (ROUTING-CLASSIFIER)")
    print(" Flow: START -> Classifier -> [Branch A | Branch B | Branch C] -> END")
    print("=" * 65)

    app = build_routing_workflow()

    # Test Query 1: Technical Issue
    query = "My server crashed with an Out of Memory error 500."
    res = app.invoke({"user_query": query})
    print(f"\nFinal Output:\n{res['response']}\n")

    print("-" * 65)

    # Test Query 2: Billing Issue
    query = "Why was I charged twice for my subscription this month?"
    res = app.invoke({"user_query": query})
    print(f"\nFinal Output:\n{res['response']}\n")

    print("=" * 65)
    print(" Routing-Classifier Workflow Completed Successfully!")
    print("=" * 65)


if __name__ == "__main__":
    main()
