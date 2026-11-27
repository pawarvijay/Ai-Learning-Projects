import os
from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(find_dotenv(usecwd=True))


def get_model(tools):
    candidates = [
        os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        "gemini-3.1-flash-lite",
        "gemini-3.6-flash",
        "gemini-3.7-flash",
        "gemini-3.5-flash",
    ]
    models = [
        ChatGoogleGenerativeAI(
            model=m,
            temperature=0,
            timeout=20,
            max_retries=0,
            max_output_tokens=150,
        ).bind_tools(tools)
        for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])
