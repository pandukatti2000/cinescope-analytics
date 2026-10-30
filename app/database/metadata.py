
from sqlalchemy import inspect

from app.database.connection import get_engine


SCHEMA_NAME = "public"


def get_table_names() -> list[str]:
    """Return the names of tables in the public schema."""
    inspector = inspect(get_engine())
    return sorted(inspector.get_table_names(schema=SCHEMA_NAME))


def get_table_columns(table_name: str) -> list[dict]:
    """Return column metadata for a table."""
    inspector = inspect(get_engine())

    if table_name not in get_table_names():
        raise ValueError(f"Unknown table: {table_name}")

    columns = inspector.get_columns(
        table_name,
        schema=SCHEMA_NAME,
    )

    return [
        {
            "name": column["name"],
            "type": str(column["type"]),
            "nullable": column["nullable"],
        }
        for column in columns
    ]


def get_primary_keys(table_name: str) -> list[str]:
    """Return the primary key columns of a table."""
    inspector = inspect(get_engine())

    if table_name not in get_table_names():
        raise ValueError(f"Unknown table: {table_name}")

    primary_key = inspector.get_pk_constraint(
        table_name,
        schema=SCHEMA_NAME,
    )

    return primary_key.get("constrained_columns", [])


def get_foreign_keys(table_name: str) -> list[dict]:
    """Return foreign key relationships for a table."""
    inspector = inspect(get_engine())

    if table_name not in get_table_names():
        raise ValueError(f"Unknown table: {table_name}")

    foreign_keys = inspector.get_foreign_keys(
        table_name,
        schema=SCHEMA_NAME,
    )

    return [
        {
            "columns": fk["constrained_columns"],
            "referenced_schema": fk["referred_schema"],
            "referenced_table": fk["referred_table"],
            "referenced_columns": fk["referred_columns"],
        }
        for fk in foreign_keys
    ]





def get_schema_description(table_names: list[str] | None = None) -> str:
    """
    Build a readable schema description containing tables,
    columns, primary keys, and foreign key relationships.
    """
    available_tables = get_table_names()

    if table_names is None:
        table_names = available_tables

    unknown_tables = set(table_names) - set(available_tables)

    if unknown_tables:
        raise ValueError(
            f"Unknown tables: {sorted(unknown_tables)}"
        )

    descriptions = []

    for table_name in table_names:
        columns = get_table_columns(table_name)
        primary_keys = get_primary_keys(table_name)
        foreign_keys = get_foreign_keys(table_name)

        lines = [f"TABLE: public.{table_name}", "COLUMNS:"]

        for column in columns:
            nullable = "NULLABLE" if column["nullable"] else "NOT NULL"

            lines.append(
                f"  - {column['name']}: {column['type']} ({nullable})"
            )

        lines.append(
            f"PRIMARY KEY: {', '.join(primary_keys) if primary_keys else 'None'}"
        )

        lines.append("FOREIGN KEYS:")

        if not foreign_keys:
            lines.append("  - None")

        for fk in foreign_keys:
            source_columns = ", ".join(fk["columns"])
            target_columns = ", ".join(fk["referenced_columns"])
            target_schema = fk["referenced_schema"] or "public"

            lines.append(
                f"  - ({source_columns}) REFERENCES "
                f"{target_schema}.{fk['referenced_table']} "
                f"({target_columns})"
            )

        descriptions.append("\n".join(lines))

    return "\n\n".join(descriptions)
