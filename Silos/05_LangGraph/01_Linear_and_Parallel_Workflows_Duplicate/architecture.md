# Architecture: Linear-Sequential

```
[ User Prompt ]
       │
       ▼
┌──────────────────┐
│    LangGraph     │ StateGraph(ChainState)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    LangChain     │ ChatGoogleGenerativeAI (invoke)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Linear Pipeline │ Outline -> Draft -> Summarize
└──────────────────┘
```

```mermaid
graph TD
    START --> outline[Step 1: Outline]
    outline --> draft[Step 2: Draft]
    draft --> summarize[Step 3: Summarize]
    summarize --> END
```
