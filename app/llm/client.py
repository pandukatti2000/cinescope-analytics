
"""
Centralized OpenAI language model configuration.
"""

from functools import lru_cache

from langchain_openai import ChatOpenAI

from app.core.config import get_settings


@lru_cache(maxsize=1)
def get_llm() -> ChatOpenAI:
    """
    Return a configured ChatOpenAI instance.

    The instance is cached so application components
    can reuse the same model configuration.
    """
    settings = get_settings()

    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key.get_secret_value(),
        temperature=0,
        max_tokens=1024,
        timeout=30,
        max_retries=2,
    )
