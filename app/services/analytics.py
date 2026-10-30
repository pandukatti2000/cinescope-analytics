
"""
Coordinate SQL generation, execution, and answer generation.
"""

from typing import Any

from app.llm.sql_generator import generate_sql
from app.llm.answer_generator import generate_answer
from app.database.executor import execute_query


def analyze_question(question: str) -> dict[str, Any]:
    """
    Analyze a natural-language business question.

    Returns the answer, database results, and SQL metadata.
    """
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Generate SQL using the LLM.
    generated_sql = generate_sql(question)

    # Step 2: Validate and execute the SQL.
    results = execute_query(generated_sql)

    # Step 3: Explain the database results.
    answer = generate_answer(
        question=question,
        sql_query=generated_sql,
        results=results,
    )

    return {
        "question": question,
        "answer": answer,
        "results": results,
        "row_count": len(results),
        "sql": generated_sql,
    }
