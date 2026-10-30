
"""
Generate PostgreSQL SQL from natural-language questions.

This module generates SQL only.
It does not execute queries against the database.
"""

from app.llm.client import get_llm
from app.llm.prompts import build_sql_prompt


def generate_sql(
    question: str,
    conversation_history: str = "",
) -> str:
    """
    Generate a SQL query using the configured OpenAI model.
    """
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    prompt = build_sql_prompt(
    question.strip(),
    conversation_history=conversation_history,
)

    llm = get_llm()
    response = llm.invoke(prompt)

    sql_query = response.content

    if not isinstance(sql_query, str):
        raise ValueError("Expected a text response from the model.")

    return sql_query.strip()
