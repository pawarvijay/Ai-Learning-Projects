import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(find_dotenv(usecwd=True))

def main():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        max_output_tokens=30,
        temperature=0
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an ultra-concise assistant. Answer in under 8 words."),
        ("human", "Explain {topic} in one short sentence.")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"topic": "LangChain Prompts"})
    print(f"Output: {result.content}")

if __name__ == "__main__":
    main()
