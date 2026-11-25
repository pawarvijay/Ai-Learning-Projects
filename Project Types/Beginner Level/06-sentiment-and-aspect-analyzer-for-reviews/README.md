# E-Commerce Review Sentiment & Aspect Analyzer

## 📌 Project Overview
**Title:** E-Commerce Review Sentiment & Aspect Analyzer  
**Industry Category:** Customer experience analytics for Amazon, Shopify, and Trustpilot reviews.  

### 📝 Description
Analyzes batch customer feedback to extract fine-grained sentiment across product dimensions (Price, Delivery, Quality, Usability).

---

## 💼 Enterprise & Industry Use Case
Customer experience analytics for Amazon, Shopify, and Trustpilot reviews.

---

## 🎯 Interview Skills Tested
Aspect-based sentiment classification, batch processing, JSON array generation.

---

## 📦 Required Packages & Libraries
- `langchain-google-genai` (Batch LLM invocation)
- `pydantic` (AspectSentiment schema validation)
- `pandas` (Tabular aggregation and CSV report generation)
- `matplotlib` / `seaborn` (Visual sentiment distribution charts)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +---------------------+
| Customer Reviews   | ----> | Aspect Sentiment AI  | ----> | Dimension Breakdown |
| (Batch Text Data)  |       |                      |       | (Price, Quality, etc)|
+--------------------+       +----------------------+       +---------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Customer Reviews (CSV) ] ──► [ Batch Processing Loop ]
                                            │
                                            ▼
                               [ Aspect Extraction Prompt ]
                               ├── Shipping & Delivery
                               ├── Product Build Quality
                               ├── Pricing & Value
                               └── Customer Service
                                            │
                                            ▼
                               [ Gemini Structured JSON ]
                                            │
                                            ▼
                               [ Aggregated Pandas Dashboard ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. pandas.read_csv('reviews.csv') loads customer comments
2. Schema defined: List[AspectRating(aspect=str, sentiment='POS'|'NEG'|'NEU', evidence=str)]
3. LLM executes batch processing with low temperature (0.0)
4. Model maps input sentences to explicit domain aspects
5. JSON parsed into pandas DataFrame
6. Summary computed: Net Sentiment Score per product dimension
```
