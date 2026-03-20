import asyncpg
import asyncio
from .config import settings

pool = None


async def get_pool():
    global pool

    if pool:
        return pool

    for _ in range(30):
        try:
            pool = await asyncpg.create_pool(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                min_size=1,
                max_size=10
            )

            print("✅ Database connected")
            return pool

        except Exception as e:
            print("Retry DB connection", e)
            await asyncio.sleep(2)

    raise Exception("Database connection failed")