import os
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    """Return an OpenAI chat model if configured; otherwise None."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0, api_key=api_key)
    except Exception:
        return None
