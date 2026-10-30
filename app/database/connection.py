
from functools import lru_cache

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, URL

from app.core.config import get_settings


@lru_cache
def get_engine() -> Engine:
    """
    Create and reuse the PostgreSQL SQLAlchemy engine.
    """
    settings = get_settings()

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=settings.db_user,
        password=settings.db_password.get_secret_value(),
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    )

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
    )

    return engine


def test_connection() -> dict:
    """
    Test PostgreSQL connectivity and return safe database details.
    """
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT
                    current_database() AS database_name,
                    current_user AS database_user,
                    version() AS postgres_version
                """
            )
        ).mappings().one()

    return dict(result)
