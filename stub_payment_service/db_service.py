import asyncpg

from .configs.config import get_settings


async def get_db_connection() -> asyncpg.connection.Connection:
    settings = get_settings()
    conn = await asyncpg.connect(user=settings.db_user, password=settings.db_password,
                                 database=settings.db_name, host=settings.db_host, port=settings.db_port)
    return conn
