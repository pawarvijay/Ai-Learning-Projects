from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(find_dotenv(usecwd=True))

def main():
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", max_output_tokens=30, temperature=0)
    prompt = ChatPromptTemplate.from_template("Translate {word} to Spanish in 1 word.")
    chain = prompt | llm | StrOutputParser()
    res = chain.invoke({"word": "hello"})
    print(f"LCEL Result: {res.strip()}")

if __name__ == "__main__":
    main()
