from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(find_dotenv(usecwd=True))

def main():
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", max_output_tokens=30, temperature=0)
    history = [
        HumanMessage(content="My name is Alex."),
        AIMessage(content="Hello Alex.")
    ]
    history.append(HumanMessage(content="What is my name? Answer in 1 word."))
    res = llm.invoke(history)
    print(f"Memory Recall: {res.content.strip()}")

if __name__ == "__main__":
    main()
