from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.admin_panel.admin_help_func import get_player_vip_panel
from keyboard.keyboard import show_vip_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards

router = Router()


@router.callback_query(F.data == 'vip_data')
async def show_vip_keyboard_func(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    user_name = callback.from_user.full_name
    user_info = {
        'telegram_id': user_id,
        'name': user_name
    }

    checked_vip_list = get_player_vip_panel(user_info)
    if checked_vip_list:
        await callback.message.answer('❕Выберите функцию:', reply_markup=make_row_inline_keyboards(show_vip_keyboard))

    else:
        await callback.message.answer(
            f'❌{callback.from_user.full_name}({callback.from_user.id}) вы не можете получить доступ к Vip Panel данного бота! Так как не являетесь Пользователем!')


@router.callback_query(F.data == 'more_stop_vip_panel')
async def more_send_stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('❕Выберите функцию', reply_markup=make_row_inline_keyboards(show_vip_keyboard))
