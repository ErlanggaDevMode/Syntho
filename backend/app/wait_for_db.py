import asyncio
import logging
import sys
from sqlalchemy import text
from app.core.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wait_for_db")


async def check_db():
    logger.info("Waiting for database connection...")
    retries = 20
    while retries > 0:
        try:
            # Try to connect and execute a simple select 1
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Database is online and responding!")
            return True
        except Exception as e:
            logger.warning(
                f"Database connection failed, retrying in 2 seconds... (error: {e})"
            )
            await asyncio.sleep(2)
            retries -= 1
    logger.error("Could not connect to database after several retries.")
    return False


if __name__ == "__main__":
    success = asyncio.run(check_db())
    if not success:
        sys.exit(1)
