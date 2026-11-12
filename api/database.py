from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from api.config import settings

engine = create_async_engine(settings.database_url, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    """Dépendance FastAPI : fournit une session par requête."""
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """Crée les tables (dev seulement — on utilisera Alembic en prod)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
