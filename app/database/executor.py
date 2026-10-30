
"""
Execute validated, read-only PostgreSQL queries.
"""

from typing import Any

from sqlalchemy import text

from app.database.connection import get_engine
from app.database.validator import validate_sql


STATEMENT_TIMEOUT_MS = 5000


def execute_query(sql_query: str) -> list[dict[str, Any]]:
    """
    Validate and execute a SQL query in a read-only transaction.

    Returns:
        Query results as a list of dictionaries.
    """
    validated_sql = validate_sql(sql_query)

    engine = get_engine()

    with engine.connect() as connection:
        try:
            # PostgreSQL transaction-level protections.
            connection.execute(text("SET TRANSACTION READ ONLY"))

            connection.execute(
                text(
                    f"SET LOCAL statement_timeout = {STATEMENT_TIMEOUT_MS}"
                )
            )

            # Execute only after validation and protections.
            result = connection.execute(text(validated_sql))

            rows = [dict(row) for row in result.mappings().all()]

            return rows

        finally:
            # End the transaction without committing changes.
            connection.rollback()
