# CSV Data Analyst & Insights Generator

## 📌 Project Overview
**Title:** CSV Data Analyst & Insights Generator  
**Industry Category:** Automated weekly reporting and ad-hoc data analysis.  

### 📝 Description
Loads a tabular CSV dataset, inspects schema and summary statistics, and generates executive business insights and trends.

---

## 💼 Enterprise & Industry Use Case
Automated weekly reporting and ad-hoc data analysis.

---

## 🎯 Interview Skills Tested
Data schema inspection, tabular grounding, trend synthesis.

---

## 📦 Required Packages & Libraries
- `pandas` (Dataframe loading, cleaning, and describe() statistics)
- `langchain-google-genai` (Statistical synthesis and insights)
- `tabulate` (Clean ASCII table formatting for prompt grounding)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +--------------------+
| Raw CSV Dataset    | ----> | Tabular Data Analyst | ----> | Executive Insights |
| (Sales/Metrics)    |       |                      |       | & Key Trends       |
+--------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Raw CSV File ] ──► [ Pandas Dataframe ]
                              │
                              ▼
                   [ Statistical Profiler ]
                   - df.info(), df.describe()
                   - Top outliers and correlations
                              │
                              ▼
                   [ LLM Insight Synthesizer ]
                              │
                              ▼
                   [ 5 Actionable Executive Takeaways ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. pandas.read_csv('sales.csv') loads data into memory
2. Compute summary metrics: total revenue, top-selling category, month-over-month growth
3. Format summary metrics into concise markdown string
4. Send to Gemini with prompt: "Synthesize 3 key trends and 2 risks from these statistics."
5. Output formatted as an executive briefing note
```
