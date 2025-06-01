import asyncio
import logging
from typing import Optional, Union

from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database.database_sqlalchemy import AsyncSessionLocal
from database.models_sqlalchemy import User, Admins, Groups


async def write_user(username: str,
                     fullname: str,
                     firstname: str,
                     lastname: str,
                     telegram_id: int,
                     async_session_factory: AsyncSessionLocal = AsyncSessionLocal) -> User:
    """
    Функция на добавления пользователя в базу данных пользователей.
    :param username: Будет храниться USERNAME пользователя
    :param fullname: Будет храниться FULLNAME Пользователя
    :param firstname: Будет храниться FIRSTNAME Пользователя
    :param lastname: Будет храниться LASTNAME Пользователя
    :param telegram_id: будет храниться TELEGRAM_ID Пользователя
    :param async_session_factory: Асинхронная Фабрика сессий
    :return:

    Examples:
        await write_user('Магомед', 'Магомед Тутуев', 'Магомед', 'Тутуев', 500)

    """

    async with async_session_factory() as session:
        try:
            user = User(username=username, fullname=fullname, firstname=firstname, lastname=lastname, telegram_id=telegram_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            logging.info(f'Пользователь добавлен! {user=}')
            return user

        except SQLAlchemyError:
            await session.rollback()
            logging.warning(f"Пользователь с таким {telegram_id=} уже существует!")


async def user_exists(telegram_id: int, async_session_factory: AsyncSessionLocal = AsyncSessionLocal) -> bool:
    """
    Функция на просмотр, есть ли пользователь с таким ID или нет.
    :param telegram_id: Ожидается telegram_id пользователя, по которому будем идти проверка, существует такой user или нет.
    :param async_session_factory: Асинхронная Фабрика сессий
    :return:

    Examples:
        print(await user_exists(567898765))

    """

    async with async_session_factory() as session:
        stmt = select(exists().where(User.telegram_id == telegram_id))
        result = await session.execute(stmt)
        return result.scalar()


async def main():
    pass




asyncio.run(main())
