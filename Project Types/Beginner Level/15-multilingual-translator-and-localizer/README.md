# Contextual Language Translator & Localizer

## 📌 Project Overview
**Title:** Contextual Language Translator & Localizer  
**Industry Category:** SaaS internationalization (i18n) and cross-border customer service.  

### 📝 Description
Translates UI copy or marketing messages across multiple languages while preserving regional idioms and technical terminology.

---

## 💼 Enterprise & Industry Use Case
SaaS internationalization (i18n) and cross-border customer service.

---

## 🎯 Interview Skills Tested
Domain-specific translation, glossary enforcement, few-shot formatting.

---

## 📦 Required Packages & Libraries
- `langchain-google-genai` (Multilingual LLM translation)
- `pydantic` (Translation dictionary schema)
- `json` (Exporting standard i18n JSON translation files)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +--------------------+
| English UI String  | ----> | Context-Aware        | ----> | Localized JSON     |
| & Target Language  |       | Localizer            |       | for Spanish/French |
+--------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Source Strings ] ──┬──► [ Context & Glossary Injector ]
                     │          (Do not translate brand names: e.g. "CloudPay")
[ Target Locales ] ──┘                    │
                                          ▼
                              [ Gemini Multilingual LLM ]
                                          │
                                          ▼
                              [ Validated i18n JSON Bundle ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Load source strings: {"login_cta": "Sign in to continue"}
2. Inject glossary constraints: "Keep company brand name in English; adapt idioms for locale."
3. Request translation for target locales (e.g., 'es-ES', 'fr-FR', 'de-DE')
4. Model generates localized strings matching native phrasing
5. Verify placeholders ({username}, %d) remain intact
6. Write out `es.json`, `fr.json` standard translation dictionaries
```
