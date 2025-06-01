import asyncio
import logging
from typing import Optional, Union

from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.util import await_only

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


async def select_to_table(telegram_id: int, async_session_factory: AsyncSessionLocal = AsyncSessionLocal) -> Optional[dict]:
    """
    Функция возвращает информацию о пользователе
    :param telegram_id: Ожидается telegram_id пользователя, по которому будет получаться вся информация из БД
    :param async_session_factory: Асинхронная Фабрика сессий
    :return:

    Examples:
        print(await select_to_table(111222))

    """

    async with async_session_factory() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            return {
                "id": user.id,
                "username": user.username,
                "fullname": user.fullname,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "telegram_id": user.telegram_id,
                "registration_date": user.registration_date.isoformat()
            }

        else:
            logging.error(f'Пользователь с {telegram_id=} не существует!')
            return {}


async def add_admin(telegram_id: int,
                    async_session_factory: AsyncSessionLocal = AsyncSessionLocal) -> Optional[Admins]:
    """
    Функция на добавление Администратора
    :param telegram_id: Ожидается telegram_id пользователя, которому выдается роль Администратора
    :param async_session_factory: Асинхронная Фабрика сессий
    :return:

    Examples:
        await add_admin(5000000)

    """

    async with async_session_factory() as session:
        try:
            admin = Admins(telegram_id=telegram_id)
            session.add(admin)
            await session.commit()
            await session.refresh(admin)
            logging.info(f'Администратор {telegram_id=} успешно добавлен!')
            return admin

        except SQLAlchemyError:
            await session.rollback()
            logging.warning(f'Такой администратор уже находится в базе данных: {admin}')


async def remove_admin(telegram_id: int,
                       async_session_factory: AsyncSessionLocal = AsyncSessionLocal):
    """
    Удаляет администратора из базы данных по telegram_id.
    :param telegram_id: ID администратора для удаления
    :param async_session_factory: Асинхронная фабрика сессий
    :return: Удаленный объект администратора или None если не найден

    Examples:
        await remove_admin(500)
    """

    async with async_session_factory() as session:
        try:
            stmt = select(Admins).where(Admins.telegram_id == telegram_id)
            result = await session.execute(stmt)
            delete_user = result.scalar_one_or_none()

            if delete_user:
                await session.delete(delete_user)
                await session.commit()
                logging.info(f'Пользователь с {telegram_id=} Успешно удален!')
                return delete_user

            else:
                logging.warning(f"Администратор {telegram_id=} не найден")
                return None

        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(f"Ошибка БД при удалении {telegram_id=}: {str(e)}")


async def get_admin_list(async_session_factory: AsyncSessionLocal = AsyncSessionLocal) -> list[int]:
    """
    Возвращает список ID администраторов или пустой список, если администраторов нет.

    :param async_session_factory: Асинхронная фабрика сессий SQLAlchemy.
    :return: list[int] – список Telegram ID администраторов.

    Examples:
    1
        print(await get_admin_list())
    2
        await get_admin_list()
    """

    async with async_session_factory() as session:
        try:

            stmt = select(Admins.telegram_id).where()
            result = await session.execute(stmt)
            admin_ids = result.scalars().all()

            if admin_ids:
                logging.info(f'Администраторы получены.')
            else:
                logging.warning('В базе нет администраторов!')

            # Вернуть список администрации или пустой список

            return admin_ids

        except SQLAlchemyError as e:
            logging.error(f'Ошибка при получении списка администрации: {e}')
            await session.rollback()
            return []


async def add_group(info_group: dict[str, str], async_session_factory: AsyncSessionLocal = AsyncSessionLocal) -> bool:
    """
    :param info_group: Словарь с данными группы {
        "username": Имя телеграм-канала (обязательно),
        "name": Имя для отображения в кнопке (обязательно)
    }
    :return:
        - True: группа успешно добавлена,
        - False: группа уже существует,

    :param async_session_factory: Асинхронная фабрика сессий SQLAlchemy.

    Examples:
        1:
            await add_group(dict)

        2:
            print(await add_group(data: username, name)) -> True or False
    """

    async with async_session_factory() as session:
        try:
            # Получение данных группы из словаря.
            username = info_group.get("username")
            name = info_group.get("name")

            if username and name:
                add_new_group = Groups(username=username, name=name)
                session.add(add_new_group)
                await session.commit()
                logging.info(f'Канал под названием: {username=} | {name=}. Успешно добавлен!')
                return True

            else:
                logging.error("Ошибка: username или name пусты")
                return False

        except IntegrityError:
            await session.rollback()
            logging.error(f"Группа <{username=}> уже существует (IntegrityError)")
            return False

        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(f"Ошибка БД при добавлении группы <{username=}: {e}>")


async def remove_group(username: str, async_session_factory: AsyncSessionLocal = AsyncSessionLocal) -> bool:
    """
    Функция по удалению канала телеграмм по username канала.

    :param username: группы по которому будет происходить удаление.
    :param async_session_factory: Асинхронная фабрика сессий SQLAlchemy.
    :return:
        - True: успешное удаление группы
        - False: в случаи если нет такой группы

    Examples:
    1
        await remove_group('Fatima_chanel1')
    2
        print(await remove_group('Fatima_chanel1'))


    """

    async with async_session_factory() as session:
        try:
            stmt = select(Groups).where(Groups.username == username)
            result = await session.execute(stmt)
            delete_group = result.scalar_one_or_none()

            if delete_group:
                await session.delete(delete_group)
                await session.commit()
                logging.info(f'Группа с {username=} успешно удалена!')
                return True

            else:
                logging.warning(f"Группа {username=} не найдена!")

        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(f"Ошибка БД при удалении {username=}: {str(e)}")


async def load_group(async_session_factory: AsyncSessionLocal = AsyncSessionLocal) -> list[dict[str, str]]:
    """

    :param async_session_factory: Асинхронная фабрика сессий SQLAlchemy.
    :return: Вернет список из словаря в котором находятся данные канала.
        [
            {
                "username": "username_group",
                "name": "name_group"
            }
        ]


    Examples: Использование
    1
        await load_group()
    2
        print(await load_group())
    """

    async with async_session_factory() as session:
        try:
            stmt = select(Groups.username, Groups.name)
            result = await session.execute(stmt)
            groups = result.mappings().all()  # Автоматические словари

            if groups:
                logging.info(f'Получено групп: {len(groups)}')
                return list(groups)
            else:
                logging.warning('В БД нет групп')
                return []

        except SQLAlchemyError as e:
            logging.error(f"Ошибка БД: {e}")
            await session.rollback()
            return []


async def main():
    # await add_group({"username": 'sdfjd', "name": '345'})
    # print(await load_group())
    pass


asyncio.run(main())
