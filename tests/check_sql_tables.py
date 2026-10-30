
"""
Test SQL table and schema restrictions.
"""

from app.database.validator import (
    SQLValidationError,
    validate_sql,
)


TEST_CASES = [
    (
        "Allowed film table",
        "SELECT title FROM public.film LIMIT 5",
        True,
    ),
    (
        "Allowed payment table",
        "SELECT SUM(amount) FROM public.payment",
        True,
    ),
    (
        "Allowed join",
        """
        SELECT f.title, COUNT(r.rental_id)
        FROM public.film f
        JOIN public.inventory i
            ON f.film_id = i.film_id
        JOIN public.rental r
            ON i.inventory_id = r.inventory_id
        GROUP BY f.title
        LIMIT 5
        """,
        True,
    ),
    (
        "PostgreSQL system schema",
        "SELECT * FROM pg_catalog.pg_roles",
        False,
    ),
    (
        "Unknown table",
        "SELECT * FROM public.secret_table",
        False,
    ),
    (
        "Unknown table without schema",
        "SELECT * FROM secret_table",
        False,
    ),
    (
        "Information schema",
        "SELECT * FROM information_schema.tables",
        False,
    ),
]


def main() -> None:
    passed = 0

    for name, query, expected_acceptance in TEST_CASES:
        try:
            validate_sql(query)
            accepted = True
        except SQLValidationError:
            accepted = False

        success = accepted == expected_acceptance

        print(f"{name}: {'PASS' if success else 'FAIL'}")

        if success:
            passed += 1

    print("-" * 40)
    print(f"Tests passed: {passed}/{len(TEST_CASES)}")

    if passed != len(TEST_CASES):
        raise SystemExit("Table validation tests failed.")


if __name__ == "__main__":
    main()
