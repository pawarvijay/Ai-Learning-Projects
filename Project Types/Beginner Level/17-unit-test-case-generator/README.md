# Automated Unit Test Case Generator

## 📌 Project Overview
**Title:** Automated Unit Test Case Generator  
**Industry Category:** Developer productivity suites and automated code review.  

### 📝 Description
Analyzes Python/Node.js utility functions and outputs comprehensive test suites covering edge cases, null inputs, and happy paths.

---

## 💼 Enterprise & Industry Use Case
Developer productivity suites and automated code review.

---

## 🎯 Interview Skills Tested
Code AST reasoning, boundary-value analysis, test framework syntax.

---

## 📦 Required Packages & Libraries
- `pytest` / `unittest` (Target Python test execution)
- `langchain-google-genai` (Code generation with Gemini)
- `pydantic` (Test suite structure validation)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +--------------------+
| Source Code        | ----> | Automated Test       | ----> | Executable Pytest  |
| Function           |       | Generator            |       | Test Suite         |
+--------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Source Function Snippet ] ──► [ Function Signature & Logic Analyzer ]
                                                  │
                                                  ▼
                                      [ Test Scenario Planner ]
                                      ├── Happy Path Cases
                                      ├── Boundary & Edge Cases
                                      └── Exception & Type Handling
                                                  │
                                                  ▼
                                      [ Gemini Code Generator ]
                                                  │
                                                  ▼
                                      [ test_*.py Test Suite ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Read target function: e.g. `def calculate_discount(price, tier): ...`
2. Prompt instructs LLM: "Write 4 pytest functions covering: normal case, 0 price, negative price, invalid tier."
3. Model outputs pure executable Python test code
4. Save to `test_suite.py`
5. Optional execution validation: subprocess.run(['pytest', 'test_suite.py'])
```
