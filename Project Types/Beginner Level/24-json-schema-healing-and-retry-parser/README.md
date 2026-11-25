# Self-Healing JSON Schema Parser (Output Repair)

## 📌 Project Overview
**Title:** Self-Healing JSON Schema Parser (Output Repair)  
**Industry Category:** High-reliability backend services consuming structured LLM outputs.  

### 📝 Description
Fixes malformed LLM JSON outputs (truncated responses, missing closing braces, unescaped quotes) automatically using repair algorithms and LLM correction passes.

---

## 💼 Enterprise & Industry Use Case
High-reliability backend services consuming structured LLM outputs.

---

## 🎯 Interview Skills Tested
Output parsing defense, JSON recovery algorithms, OutputFixingParser.

---

## 📦 Required Packages & Libraries
- `json` (Standard parser)
- `json-repair` / `dirtyjson` (Heuristic JSON repair library for syntax flaws)
- `langchain-core` (OutputFixingParser with secondary LLM pass)
- `pydantic` (Target validation schema)

---

## ⚠️ Real-World Edge Cases & Failure Modes
- **Critical Failure Mode:** Production outages, runaway token bills, and prompt injection exploits.
- **Defensive Mechanism:** Built specifically to catch, isolate, and mitigate failure modes before they reach core business logic.

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +--------------------+
| Broken / Truncated | ----> | Self-Healing JSON    | ----> | Valid, Strictly    |
| LLM JSON Output    |       | Repair Engine        |       | Typed Python Object|
+--------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Raw LLM Output (Truncated/Broken) ] ──► [ json.loads() Attempt ]
                                                      │
                                      ┌───────────────┴───────────────┐
                                      ▼ (Valid)                       ▼ (JSONDecodeError)
                              [ Target Pydantic ]            [ Heuristic Auto-Repair ]
                                                             (Balance braces, fix quotes)
                                                                      │
                                                      ┌───────────────┴───────────────┐
                                                      ▼ (Heuristic Pass)              ▼ (Heuristic Fail)
                                              [ Target Pydantic ]            [ OutputFixingParser Pass ]
                                                                             (LLM heals its own output)
                                                                                      │
                                                                                      ▼
                                                                             [ Validated Object ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. LLM returns truncated output: `{"order_id": 42, "items": ["item1", "item` (cut off by token limit)
2. json.loads() throws json.decoder.JSONDecodeError
3. Stage 1: Fast zero-cost repair using json_repair.repair_json(raw_string)
4. If Pydantic validation still fails: Stage 2 OutputFixingParser.from_llm(llm=llm, parser=parser)
5. Secondary prompt passes broken string + parser error trace back to model: "Fix syntax to match schema."
6. Verified Pydantic object returned safely to application
```
