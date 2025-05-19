import asyncio
import logging
from typing import Optional

from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database.database_sqlalchemy import AsyncSessionLocal
from database.models_sqlalchemy import User, Admins


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
            logging.info(f'Пользователь добавлен! {user}')
            return user

        except SQLAlchemyError:
            await session.rollback()
            logging.warning(f"Пользователь с таким telegram_id={telegram_id} уже существует!")



