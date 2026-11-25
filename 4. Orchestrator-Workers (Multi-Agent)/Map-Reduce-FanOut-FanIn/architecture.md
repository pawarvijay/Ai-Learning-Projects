# Architecture: Map-Reduce-FanOut-FanIn

```
[ Large Document Set / Data Chunks ]
                 │
                 ▼
┌─────────────────────────────────┐
│            LangGraph            │ StateGraph(MapReduceState)
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│            LangChain            │ ChatGoogleGenerativeAI (Map + Reduce)
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│      Map-Reduce Architecture    │ Map Workers (Chunk 1..N) ──► Reduce Synthesizer ──► END
└─────────────────────────────────┘
```

```mermaid
graph TD
    START --> map1[Map Worker: Chunk 1]
    START --> map2[Map Worker: Chunk 2]
    map1 --> reduce[Reduce Synthesizer Node]
    map2 --> reduce
    reduce --> END
```
