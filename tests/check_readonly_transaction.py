
"""
Verify PostgreSQL read-only transaction configuration.

This test does not attempt to modify database records.
"""

from sqlalchemy import text

from app.database.connection import get_engine


def main() -> None:
    engine = get_engine()

    with engine.connect() as connection:
        # Start a transaction in read-only mode.
        connection.execute(
            text("SET TRANSACTION READ ONLY")
        )

        result = connection.execute(
            text(
                """
                SELECT
                    current_user AS database_user,
                    current_setting('transaction_read_only')
                        AS transaction_read_only,
                    COUNT(*) AS total_films
                FROM public.film
                """
            )
        ).mappings().one()

        print("Database user:", result["database_user"])
        print(
            "Transaction read-only:",
            result["transaction_read_only"],
        )
        print("Total films:", result["total_films"])

        # Roll back when finished.
        connection.rollback()


if __name__ == "__main__":
    main()
