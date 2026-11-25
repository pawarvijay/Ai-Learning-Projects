# Architecture: Parallel-ReAct-Swarm

```
[ Target Company / Entity ]
              │
              ▼
┌───────────────────────────┐
│         LangGraph         │ StateGraph(SwarmState)
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│         LangChain         │ Specialized Agents with discrete Tools
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│    Parallel Agent Swarm   │ [ News Agent (Tools) | Financial Agent (Tools) ]
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│        Aggregator         │ Merges parallel agent tool findings into single report
└─────────────┬─────────────┘
              │
              ▼
           [ END ]
```

```mermaid
graph TD
    START --> news_agent[News Agent: fetch_news tool]
    START --> finance_agent[Finance Agent: fetch_stock tool]
    news_agent --> aggregator[Executive Synthesizer]
    finance_agent --> aggregator
    aggregator --> END
```
