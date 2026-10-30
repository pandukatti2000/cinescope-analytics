
"""
Validate LLM-generated SQL before database execution.
"""

import sqlglot
from sqlglot import exp
from app.database.metadata import get_table_names

class SQLValidationError(ValueError):
    """Raised when generated SQL fails validation."""


FORBIDDEN_EXPRESSIONS = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Create,
    exp.Alter,
    exp.TruncateTable,
    exp.Command,
    exp.Into,
)

ALLOWED_FUNCTIONS = {
    "COUNT",
    "SUM",
    "AVG",
    "MIN",
    "MAX",
    "ROUND",
    "COALESCE",
    "NULLIF",
    "LOWER",
    "UPPER",
    "TRIM",
    "LENGTH",
    "ABS",
    "DATE_TRUNC",
    "EXTRACT",
    "TO_CHAR",
    "TIMESTAMP_TRUNC",
}


def validate_sql(sql_query: str) -> str:
    """
    Accept only one PostgreSQL SELECT statement.

    This is an initial validation layer, not a complete
    database security boundary.
    """
    if not sql_query or not sql_query.strip():
        raise SQLValidationError("SQL query cannot be empty.")

    try:
        statements = sqlglot.parse(
            sql_query,
            read="postgres",
            error_level="RAISE",
        )
    except sqlglot.errors.ParseError as exc:
        raise SQLValidationError(
            f"Invalid SQL syntax: {exc}"
        ) from exc

    if len(statements) != 1 or statements[0] is None:
        raise SQLValidationError(
            "Exactly one SQL statement is allowed."
        )

    statement = statements[0]

    if not isinstance(statement, exp.Select):
        raise SQLValidationError(
            "Only SELECT statements are allowed."
        )

        # Reject SELECT statements that request row-level locks.
    for select_node in statement.find_all(exp.Select):
        if select_node.args.get("locks"):
            raise SQLValidationError(
                "Row-locking clauses such as FOR UPDATE are not allowed."
            )

    for node in statement.walk():
        if isinstance(node, FORBIDDEN_EXPRESSIONS):
            raise SQLValidationError(
                f"Forbidden SQL operation: {type(node).__name__}"
            )

        if isinstance(node, exp.Func):
            function_name = node.sql_name().upper()

            if function_name not in ALLOWED_FUNCTIONS:
                raise SQLValidationError(
                    f"Function not allowed: {function_name}"
                )

    allowed_tables = set(get_table_names())

    for table in statement.find_all(exp.Table):
        table_name = table.name
        schema_name = table.db

        if schema_name and schema_name != "public":
            raise SQLValidationError(
                f"Schema not allowed: {schema_name}"
            )

        if table_name not in allowed_tables:
            raise SQLValidationError(
                f"Table not allowed: {table_name}"
            )



    # Enforce a maximum of 100 returned rows.
    max_rows = 100
    limit_node = statement.args.get("limit")

    if limit_node is None:
        statement = statement.limit(max_rows)
    else:
        limit_value = limit_node.expression

        if not isinstance(limit_value, exp.Literal):
            raise SQLValidationError(
                "LIMIT must be a positive integer."
            )

        try:
            requested_limit = int(limit_value.this)
        except (ValueError, TypeError):
            raise SQLValidationError(
                "LIMIT must be a positive integer."
            )

        if requested_limit < 1:
            raise SQLValidationError(
                "LIMIT must be greater than zero."
            )

        if requested_limit > max_rows:
            statement = statement.limit(max_rows)

    return statement.sql(dialect="postgres")
