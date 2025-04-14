from sqlalchemy.ext.asyncio import create_async_engine
from database.models.Base import Base
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

sqlite_url = f"sqlite+aiosqlite:///database.db"
engine = create_async_engine(sqlite_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

