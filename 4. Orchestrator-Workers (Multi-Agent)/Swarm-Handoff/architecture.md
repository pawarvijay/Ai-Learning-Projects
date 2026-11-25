# Architecture: Swarm-Handoff

```
[ User Request ]
       │
       ▼
┌──────────────────┐
│    LangGraph     │ StateGraph(SwarmState)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    LangChain     │ ChatGoogleGenerativeAI (Multi-Persona)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Peer Handoff    │ Triage Agent ──(Hands Off Context)──► Refund Specialist Agent ──► END
└──────────────────┘
```

```mermaid
graph TD
    START --> triage[Triage Front-Desk Agent]
    triage -->|peer handoff| refund[Refund Specialist Agent]
    triage -->|general inquiry| END
    refund --> END
```
