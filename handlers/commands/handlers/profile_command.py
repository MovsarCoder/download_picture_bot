from aiogram import F, Router
from aiogram.types import Message

from database.crud_sqlalchemy import select_to_table

from aiogram.filters import Command

router = Router()


@router.message(Command('profile'))
@router.message(F.text == 'ℹ️ Личная информация')
async def personal_information_func(message: Message):
    id_user = message.from_user.id
    get_id_user = await select_to_table(id_user)
    get_id_user_info = {
        "id": get_id_user.get("id"),
        "username": get_id_user.get("username"),
        "fullname": get_id_user.get("fullname"),
        "firstname": get_id_user.get('firstname'),
        "lastname": get_id_user.get('lastname'),
        "telegram_id": get_id_user.get('telegram_id'),
        "sign_up_people": get_id_user.get('sign_up_people'),
    }

    send_info_message = f"""
    📊 Статистика пользователя\n
    
ℹ️ Личная информация по пользователю "{get_id_user_info.get("id")}" \n
    
👨 Имя аккаунта: {get_id_user_info.get("username")}
👨 Полное имя: {get_id_user_info.get("fullname")}
👨 Имя пользователя: {get_id_user_info.get("firstname")} 
👨 Фамилия пользователя (Если имеется): {get_id_user_info.get("lastname")}
👨 Ваш уникальный идентификатор Telegram (ID): {get_id_user_info.get("telegram_id")}
👨 Дата регистрации в боте: {get_id_user_info.get("sign_up_people")}
    
    
    """
    await message.answer(send_info_message)
