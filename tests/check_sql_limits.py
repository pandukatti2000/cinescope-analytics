
"""
Test SQL LIMIT validation and enforcement.
"""

from app.database.validator import SQLValidationError, validate_sql


TEST_CASES = [
    ("No limit", "SELECT * FROM public.film", "LIMIT 100"),
    ("Small limit", "SELECT * FROM public.film LIMIT 5", "LIMIT 5"),
    ("Large limit", "SELECT * FROM public.film LIMIT 500", "LIMIT 100"),
]

REJECT_CASES = [
    ("LIMIT ALL", "SELECT * FROM public.film LIMIT ALL"),
    ("Negative limit", "SELECT * FROM public.film LIMIT -1"),
    ("Zero limit", "SELECT * FROM public.film LIMIT 0"),
]


def main() -> None:
    passed = 0
    total = len(TEST_CASES) + len(REJECT_CASES)

    for name, query, expected in TEST_CASES:
        try:
            result = validate_sql(query)
            success = result.endswith(expected)
        except SQLValidationError:
            success = False

        print(f"{name}: {'PASS' if success else 'FAIL'}")

        if success:
            passed += 1

    for name, query in REJECT_CASES:
        try:
            validate_sql(query)
            success = False
        except SQLValidationError:
            success = True

        print(f"{name}: {'PASS' if success else 'FAIL'}")

        if success:
            passed += 1

    print("-" * 40)
    print(f"Tests passed: {passed}/{total}")

    if passed != total:
        raise SystemExit("SQL LIMIT tests failed.")


if __name__ == "__main__":
    main()
