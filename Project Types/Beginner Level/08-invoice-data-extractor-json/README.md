# Invoice & Receipt Key-Value Extractor

## 📌 Project Overview
**Title:** Invoice & Receipt Key-Value Extractor  
**Industry Category:** Automated accounts payable and expense management (Expensify, QuickBooks).  

### 📝 Description
Extracts structured metadata (Invoice #, Date, Vendor Name, Line Items, Tax, Total Due) from unstructured receipt and invoice texts into validated JSON.

---

## 💼 Enterprise & Industry Use Case
Automated accounts payable and expense management (Expensify, QuickBooks).

---

## 🎯 Interview Skills Tested
Zero-shot extraction, Pydantic data schemas, nested JSON validation.

---

## 📦 Required Packages & Libraries
- `pypdf` / `pytesseract` (PDF/OCR text extraction)
- `pydantic` (Strict InvoiceSchema with line-item array)
- `langchain-google-genai` (Structured output extraction with Gemini)
- `json` (Standard JSON serialization and file exports)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+---------------------+       +---------------------+       +----------------------+
| Raw Invoice /       | ----> | Zero-Shot Structured| ----> | Clean, Validated     |
| Receipt Text        |       | Data Extractor      |       | JSON Database Record |
+---------------------+       +---------------------+       +----------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Invoice Text / OCR ] ──► [ Schema-Enforced Prompt ]
                                        │
                                        ▼
                            [ Gemini Flash Lite ]
                                        │
                                        ▼
                            [ Pydantic Invoice Validator ]
                            ├── vendor_name (str)
                            ├── invoice_number (str)
                            ├── line_items: List[Item(desc, qty, price)]
                            └── total_amount (float)
                                        │
                                        ▼
                            [ ERP / Accounting Database ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Ingest invoice text via file read or OCR
2. Define Pydantic schema:
   class LineItem(BaseModel):
       description: str; quantity: int; unit_price: float; total: float
   class Invoice(BaseModel):
       vendor: str; invoice_no: str; date: str; items: List[LineItem]; total: float
3. Invoke model: llm.with_structured_output(Invoice)
4. LLM analyzes raw receipt text, performing implicit entity resolution
5. Python validates currency numeric values and calculates line item math checks
6. Write validated JSON payload to output directory or database table
```
