
"""
Test natural-language-to-SQL generation.

The generated SQL is printed but never executed.
"""

from app.llm.sql_generator import generate_sql


def main() -> None:
    question = "Show the top 5 movies by total revenue."

    print("USER QUESTION:")
    print(question)

    print("\nGENERATED SQL:")
    sql_query = generate_sql(question)
    print(sql_query)


if __name__ == "__main__":
    main()
