from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.crud_sqlalchemy import get_personal_information_vip_panel

router = Router()


@router.callback_query(F.data == 'info_vip_panel')
async def get_personal_info(callback: CallbackQuery):
    await callback.answer('')
    telegram_id = callback.from_user.id
    get_information = await get_personal_information_vip_panel(telegram_id)

    if get_information:
        information = f"""
        Ваша информация в базе данных.
        
        Статус вип панели: {get_information.get("status_vip")}

        По счету добавленный в вип панель: {get_information.get("id")} \n
        Ваш уникальный идентификатор телеграмма: {get_information.get("telegram_id")} \n
        Дата покупки вип панели: {get_information.get("created_at")} \n
        Количество дней которое осталось: {get_information.get("number_of_days")} \n
        Имя: {get_information.get("name")}
        """

        await callback.message.answer(information)

    else:
        await callback.message.answer('Нет никакой информации про вас!')
