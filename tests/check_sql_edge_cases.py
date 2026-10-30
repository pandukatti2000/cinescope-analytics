
"""
Diagnose SQL constructs that require additional validation.

This test does not execute SQL against PostgreSQL.
"""

from app.database.validator import SQLValidationError, validate_sql


TEST_CASES = [
    ("Row locking", "SELECT * FROM public.film FOR UPDATE"),
    ("Unlimited rows", "SELECT * FROM public.film LIMIT ALL"),
    ("No row limit", "SELECT * FROM public.film"),
    ("CTE", "WITH movies AS (SELECT * FROM public.film) SELECT * FROM movies"),
    ("Derived table", "SELECT * FROM (SELECT * FROM public.film) AS movies"),
]


def main() -> None:
    for name, query in TEST_CASES:
        try:
            validated = validate_sql(query)
            print(f"{name}: ACCEPTED")
            print(f"  SQL: {validated}")
        except SQLValidationError as exc:
            print(f"{name}: REJECTED")
            print(f"  Reason: {exc}")


if __name__ == "__main__":
    main()
