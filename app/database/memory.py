"""
PostgreSQL checkpoint storage for CineScope conversations.
"""

from dotenv import dotenv_values
from psycopg.conninfo import make_conninfo
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver


def create_memory_checkpointer():
    """
    Create a PostgreSQL connection pool and LangGraph checkpointer.

    The caller is responsible for closing the pool.
    """
    env = dotenv_values(".env")

    connection_string = make_conninfo(
        "",
        host=env["MEMORY_DB_HOST"],
        port=env["MEMORY_DB_PORT"],
        dbname=env["MEMORY_DB_NAME"],
        user=env["MEMORY_DB_USER"],
        password=env["MEMORY_DB_PASSWORD"],
    )

    pool = ConnectionPool(
        conninfo=connection_string,
        min_size=1,
        max_size=5,
        open=False,
        kwargs={
            "autocommit": True,
            "prepare_threshold": None,
        },
    )

    checkpointer = PostgresSaver(pool)

    return pool, checkpointer