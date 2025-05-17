import asyncio
import logging

from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError

from database.database_sqlalchemy import AsyncSessionLocal
from database.models_sqlalchemy import User, Admins

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Функция на добавления пользователя в базу данных пользователей
async def write_user(username: str,
                     fullname: str,
                     firstname: str,
                     lastname: str,
                     telegram_id: int,
                     async_session_factory: AsyncSessionLocal = AsyncSessionLocal):
    """
    :param username: Будет храниться USERNAME пользователя
    :param fullname: Будет храниться FULLNAME Пользователя
    :param firstname: Будет храниться FIRSTNAME Пользователя
    :param lastname: Будет храниться LASTNAME Пользователя
    :param telegram_id: будет храниться TELEGRAM_ID Пользователя
    :param async_session_factory: Асинхронная Фабрика сессий
    :return:

    Examples:
        await write_user('DIKIIIIIII', 'Deni Bisultanov', 'Deni', 'Bisultanov', 500)

    """

    async with async_session_factory() as session:
        try:
            user = User(username=username, fullname=fullname, firstname=firstname, lastname=lastname, telegram_id=telegram_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            logging.info(f'Пользователь добавлен! {user}')
            return user

        except IntegrityError as e:
            await session.rollback()
            logger.error(f"Пользователь с таким telegram_id={telegram_id} уже существует!")
            raise ValueError(f"Пользователь с таким telegram_id={telegram_id} уже существует!") from e


