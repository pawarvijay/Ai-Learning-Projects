import os
from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from .tools import tools

load_dotenv(find_dotenv(usecwd=True))


def get_model():
    """Creates a Gemini chat model with bound tools and fallback models."""
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
            max_output_tokens=30,
        ).bind_tools(tools)
        for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


model_with_tools = get_model()
