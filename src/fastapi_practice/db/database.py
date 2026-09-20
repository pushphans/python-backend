from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from fastapi_practice.core.config import settings


engine = create_async_engine(
    url = settings.DATABASE_URL 
)



async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)




class Base(DeclarativeBase):
    pass




async def get_db():
    async with async_session_factory() as session:
        yield session