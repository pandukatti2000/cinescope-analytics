"""
Initialize PostgreSQL checkpoint storage for CineScope.
Run once before enabling persistent LangGraph memory.
"""

from dotenv import dotenv_values
from psycopg.conninfo import make_conninfo
from langgraph.checkpoint.postgres import PostgresSaver


def main():
    env = dotenv_values(".env")

    connection_string = make_conninfo(
        "",
        host=env["MEMORY_DB_HOST"],
        port=env["MEMORY_DB_PORT"],
        dbname=env["MEMORY_DB_NAME"],
        user=env["MEMORY_DB_USER"],
        password=env["MEMORY_DB_PASSWORD"],
    )

    print("Initializing LangGraph checkpoint storage...")

    with PostgresSaver.from_conn_string(connection_string) as checkpointer:
        checkpointer.setup()

    print("Checkpoint setup: SUCCESS")
    print("Database:", env["MEMORY_DB_NAME"])


if __name__ == "__main__":
    main()