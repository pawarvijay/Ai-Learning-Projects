# Personal Finance Transaction Categorizer

## 📌 Project Overview
**Title:** Personal Finance Transaction Categorizer  
**Industry Category:** Fintech consumer apps (Mint, YNAB, Revolut) and expense tracking.  

### 📝 Description
Classifies raw bank transactions into standard budget buckets (Groceries, Travel, Utilities, Dining) with monthly spend aggregation.

---

## 💼 Enterprise & Industry Use Case
Fintech consumer apps (Mint, YNAB, Revolut) and expense tracking.

---

## 🎯 Interview Skills Tested
Unstructured text categorization, merchant normalization, summary aggregation.

---

## 📦 Required Packages & Libraries
- `pandas` (Transaction data handling and monthly aggregation)
- `langchain-google-genai` (Zero-shot merchant normalization and categorization)
- `pydantic` (TransactionRecord schema validation)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+---------------------+       +----------------------+       +--------------------+
| Raw Bank Statement  | ----> | Merchant Normalizer  | ----> | Categorized Spend  |
| ("UBR*TRIP 982")    |       | & Categorizer        |       | Dashboard & Budget |
+---------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Raw Transaction Text ] ──► [ Merchant Normalization ] (UBR*TRIP -> "Uber")
                                          │
                                          ▼
                             [ Spending Category Classifier ]
                             - Categories: Travel, Food, Utilities, Subscriptions
                                          │
                                          ▼
                             [ Categorized Transaction Ledger ]
                                          │
                                          ▼
                             [ Pandas Monthly Budget Summary ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Load bank statement CSV: ['DATE', 'RAW_DESC', 'AMOUNT']
2. Process raw descriptions through LLM: "Normalize merchant and categorize into: [Dining, Travel, Groceries, Utilities, Shopping]"
3. Parse response into structured columns: Normalized_Merchant, Category
4. pandas.groupby('Category')['AMOUNT'].sum() aggregates monthly spend
5. Print clean budget breakdown table to terminal or export as JSON
```
