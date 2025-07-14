import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    database_url: str
    secret_key: str = "your-secret-key-here"  # Replace with a secure key in production

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure the DATABASE_URL uses asyncpg driver
try:
    if not settings.database_url.startswith("postgresql+asyncpg://"):
        settings.database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
    logger.info(f"Using database URL: {settings.database_url}")
except Exception as e:
    logger.error(f"Failed to process DATABASE_URL: {e}")
    raise

# Create async engine
try:
    engine = create_async_engine(settings.database_url, echo=False)
except Exception as e:
    logger.error(f"Failed to create async engine: {e}")
    raise

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
