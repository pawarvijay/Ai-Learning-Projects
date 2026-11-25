# Natural Language SQL Query Generator (Text-to-SQL)

## 📌 Project Overview
**Title:** Natural Language SQL Query Generator (Text-to-SQL)  
**Industry Category:** Self-service business intelligence (BI) for non-technical product and sales managers.  

### 📝 Description
Converts plain English business questions into syntactically valid, safe SELECT queries against an existing database schema.

---

## 💼 Enterprise & Industry Use Case
Self-service business intelligence (BI) for non-technical product and sales managers.

---

## 🎯 Interview Skills Tested
Database schema injection, SQL dialect constraints, safety guardrails (read-only validation).

---

## 📦 Required Packages & Libraries
- `sqlalchemy` (Database schema inspection and safe query execution)
- `sqlparse` (SQL formatting, syntax validation, and statement verification)
- `langchain-google-genai` (Prompt-to-SQL translation)
- `sqlite3` / `psycopg2-binary` (Underlying database engines)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+---------------------+       +----------------------+       +----------------------+
| Plain English Query | ----> | Text-to-SQL Engine   | ----> | Verified Database    |
| ("Top 5 customers") |       | (Grounded in Schema) |       | Report / Query Result|
+---------------------+       +----------------------+       +----------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ User Question ] ──┬──► [ Text-to-SQL Generator ] ──► [ Raw SQL Query ]
                     │                 │                                │
[ DB Table Schema ] ─┘                 ▼                                ▼
                               [ Gemini LLM ]                [ SQL Safety Guard ]
                                                             - Block DROP/UPDATE/DELETE
                                                             - Enforce LIMIT clauses
                                                                        │
                                                                        ▼
                                                             [ Database Engine (SQL) ]
                                                                        │
                                                                        ▼
                                                             [ Tabular Data Result ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. SQLAlchemy engine inspects target DB: inspector.get_table_names(), get_columns()
2. Assemble prompt containing DDL schema strings + business question
3. LLM instructed: "Generate ONLY a SQLite-compatible SELECT statement. Never use DROP/DELETE/INSERT."
4. Resulting string cleaned of markdown backticks
5. sqlparse.parse(query) verifies AST contains only DML SELECT statements
6. Connection executed with read-only cursor: db.execute(text(clean_sql)).fetchall()
7. Returned rows formatted into clean tabular markdown or JSON
```
