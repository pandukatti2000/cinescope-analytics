
from app.database.validator import SQLValidationError, validate_sql


TEST_CASES = [
    ("COUNT", "SELECT COUNT(*) FROM public.rental", True),
    ("SUM", "SELECT SUM(amount) FROM public.payment", True),
    ("pg_sleep", "SELECT pg_sleep(10)", False),
    ("version", "SELECT version()", False),
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
        raise SystemExit("Function validation tests failed.")


if __name__ == "__main__":
    main()
