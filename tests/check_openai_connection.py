
from langchain_openai import ChatOpenAI

from app.core.config import get_settings


def main() -> None:
    settings = get_settings()

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key.get_secret_value(),
        temperature=0,
        max_tokens=30,
        timeout=30,
        max_retries=1,
    )

    print("Testing OpenAI API connection...")
    print(f"Configured model: {settings.openai_model}")

    response = llm.invoke(
        "Reply with exactly: Movie Rental AI connection successful."
    )

    print(f"Model response: {response.content}")
    print("API request completed successfully.")


if __name__ == "__main__":
    main()
