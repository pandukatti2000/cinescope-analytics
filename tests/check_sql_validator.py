
"""
Test SQL validation for accepted and rejected statements.
"""

from app.database.validator import (
    SQLValidationError,
    validate_sql,
)


TEST_CASES = [
    ("Valid SELECT", "SELECT title FROM public.film LIMIT 5", True),
    ("DELETE statement", "DELETE FROM public.payment", False),
    ("DROP statement", "DROP TABLE public.customer", False),
    (
        "Multiple statements",
        "SELECT 1; DELETE FROM public.rental",
        False,
    ),
    ("Empty SQL", "", False),
]


def main() -> None:
    passed = 0

    for name, sql, should_accept in TEST_CASES:
        try:
            validate_sql(sql)
            accepted = True
        except SQLValidationError:
            accepted = False

        success = accepted == should_accept

        print(f"{name}: {'PASS' if success else 'FAIL'}")

        if success:
            passed += 1

    print("-" * 40)
    print(f"Tests passed: {passed}/{len(TEST_CASES)}")

    if passed != len(TEST_CASES):
        raise SystemExit("SQL validator tests failed.")


if __name__ == "__main__":
    main()
