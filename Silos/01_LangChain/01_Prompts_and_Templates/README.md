# 01_Prompts_and_Templates

Demonstrates variable injection using `ChatPromptTemplate` with strict token limits.

## Key Code
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an ultra-concise assistant. Answer in under 8 words."),
    ("human", "Explain {topic} in one short sentence.")
])
chain = prompt | llm
```

## Running
```bash
uv run start
```
