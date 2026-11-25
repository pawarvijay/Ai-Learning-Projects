import os
from typing import TypedDict
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool


class SwarmState(TypedDict):
    company: str
    news_report: str
    stock_report: str
    executive_synthesis: str


@tool
def fetch_news(company: str) -> str:
    """Searches news database."""
    return f"News: {company} announced breakthrough AI microchip."


@tool
def fetch_stock(company: str) -> str:
    """Queries live financial stock tickers."""
    return f"Stock: {company} up 4.2% at $195.40/share."


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


def news_agent(state: SwarmState) -> dict:
    print("\n[News Agent (Parallel ReAct)]: Ingesting news tools...")
    data = fetch_news.invoke({"company": state["company"]})
    prompt = f"In under 8 words, summarize market news: {data}"
    res = llm.invoke(prompt)
    ans = getattr(res, "text", res.content).strip()
    print(f"  News Agent Output: {ans}")
    return {"news_report": ans}


def financial_agent(state: SwarmState) -> dict:
    print("[Financial Agent (Parallel ReAct)]: Ingesting market ticker tools...")
    data = fetch_stock.invoke({"company": state["company"]})
    prompt = f"In under 8 words, summarize stock price: {data}"
    res = llm.invoke(prompt)
    ans = getattr(res, "text", res.content).strip()
    print(f"  Financial Agent Output: {ans}")
    return {"stock_report": ans}


def aggregator_node(state: SwarmState) -> dict:
    print("\n[Aggregator Agent]: Synthesizing parallel agent findings...")
    combined = f"{state['news_report']} | {state['stock_report']}"
    prompt = f"In under 12 words, synthesize into an investor briefing: {combined}"
    res = llm.invoke(prompt)
    synthesis = getattr(res, "text", res.content).strip()
    print(f"  Briefing: {synthesis}\n")
    return {"executive_synthesis": synthesis}


def build_parallel_react_swarm():
    workflow = StateGraph(SwarmState)
    workflow.add_node("news_agent", news_agent)
    workflow.add_node("finance_agent", financial_agent)
    workflow.add_node("aggregator", aggregator_node)

    # Parallel Fan-Out to 2 autonomous tool-using agents
    workflow.add_edge(START, "news_agent")
    workflow.add_edge(START, "finance_agent")

    # Fan-In: Both agents join into Aggregator
    workflow.add_edge("news_agent", "aggregator")
    workflow.add_edge("finance_agent", "aggregator")
    workflow.add_edge("aggregator", END)

    return workflow.compile()


def main():
    print("=" * 65)
    print(" PATTERN: 5. COMBINATION (PARALLEL-REACT-SWARM)")
    print(" Flow: START -> [News Agent | Finance Agent] (Parallel) -> Aggregator -> END")
    print("=" * 65)

    app = build_parallel_react_swarm()
    res = app.invoke({"company": "NVIDIA"})

    print("=" * 65)
    print(f"Final Briefing: {res['executive_synthesis']}")
    print("=" * 65)


if __name__ == "__main__":
    main()
