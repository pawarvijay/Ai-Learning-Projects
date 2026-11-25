# Autonomous Agent Loop Watchdog & Budget Guard

## 📌 Project Overview
**Title:** Autonomous Agent Loop Watchdog & Budget Guard  
**Industry Category:** Agentic production reliability, cloud cost containment, DoS prevention.  

### 📝 Description
Enforces strict step ceilings, token spending budgets, and wall-clock execution timeouts to prevent autonomous ReAct agents from cycling infinitely.

---

## 💼 Enterprise & Industry Use Case
Agentic production reliability, cloud cost containment, DoS prevention.

---

## 🎯 Interview Skills Tested
Loop guardrails, state-based step counters, token budget tracking, timeout decorators.

---

## 📦 Required Packages & Libraries
- `langgraph` (StateGraph with recursion_limit=10)
- `asyncio` (Wall-clock timeouts using asyncio.wait_for)
- `pydantic` (AgentState containing step_count and token_spend metrics)

---

## ⚠️ Real-World Edge Cases & Failure Modes
- **Critical Failure Mode:** Production outages, runaway token bills, and prompt injection exploits.
- **Defensive Mechanism:** Built specifically to catch, isolate, and mitigate failure modes before they reach core business logic.

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +--------------------+
| Autonomous Agent   | ----> | Budget Watchdog &    | ----> | Safe Completion or |
| Execution Loop     |       | Step-Count Guard     |       | Controlled Timeout |
+--------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ User Request ] ──► [ Agent State Machine ]
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       [ Next Agent Step ]          [ Watchdog Checks ]
                │                   ├── step_count < MAX_STEPS (e.g. 5)
                │                   ├── cumulative_tokens < BUDGET (e.g. 2000)
                │                   └── execution_time < TIMEOUT (e.g. 30s)
                │                             │
                ▼                             ▼
       [ Execute Tool Call ]         [ Threshold Exceeded? ]
                │                             │
                │                     (Yes) ──┴──► [ Force Stop / Return Partial State ]
                │
                └──────────────► [ Loop Back ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Initialize AgentState with step_count=0, total_tokens=0, start_time=time.time()
2. Graph configured with app.compile(config={"recursion_limit": 8})
3. Inside should_continue(state):
   if state['step_count'] >= 5: return 'emergency_summary'
   if time.time() - state['start_time'] > 25.0: return 'timeout_fallback'
4. LLM response usage_metadata inspected; total_tokens added to state accumulator
5. Prevents runaway billing loops and guarantees predictable SLAs
```
