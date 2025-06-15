from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboard.keyboard import back_keyboard, admin_panel_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards
from database.crud import delete_users_with_vip_panel_functions
from States.state import DeleteVipPanel

router = Router()


@router.callback_query(F.data == 'delete_user_with_vip_panel')
async def delete_user_vip_panel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите ID пользователя:', reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(DeleteVipPanel.get_id)


@router.message(DeleteVipPanel.get_id)
async def delete_user_vip_panel_fsm(message: Message, state: FSMContext):
    user_get_text = message.text
    user_name = ''

    data = {
        'telegram_id': user_get_text,
        'name': user_name
    }

    if delete_users_with_vip_panel_functions(data):
        await message.answer('✅Человек успешно удален из списка Vip пользователей!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
    else:
        await message.answer('⚠️Такого пользователя нет в списке Vip пользователей!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

    await state.clear()
