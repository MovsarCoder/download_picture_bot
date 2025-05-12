from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs, async_sessionmaker

engine = create_async_engine('sqlite+aiosqlite:///users.db', echo=True, pool_size=10) # Делаем подключение

# AsyncSessionLocal = sessionmaker(bind=engine, expire_on_commit=False) # Фабрика сессий
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False) # Фабрика сессий


# Base = declarative_base()
class Base(AsyncAttrs, DeclarativeBase):
    pass

# Base.metadata.create_all(engine) # Создай все таблицы

