from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == 'info_vip_panel')
async def get_personal_info(callback: CallbackQuery):
    await callback.answer('')

    await callback.message.answer("Ваша личная информация про вип панель!")
