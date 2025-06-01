from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs, async_sessionmaker
from config.settings import DATABASE_URL

# async_engine = create_async_engine(DATABASE_URL)
async_engine = create_async_engine('sqlite+aiosqlite:///users.db', echo=True, pool_size=10) # Делаем подключение


# AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession expire_on_commit=False) # Фабрика сессий
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False) # Асинхронная фабрика сессий


# Base = declarative_base()
class Base(AsyncAttrs, DeclarativeBase):
    pass


# НЕ ДЛЯ АССИНХРОННОСТИ!
# Base.metadata.create_all(engine) # Создай все таблицы

