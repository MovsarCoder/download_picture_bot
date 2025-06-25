from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboard.keyboard import back_keyboard, admin_panel_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards
from States.state import AdminState
from database.crud_sqlalchemy import remove_admin

router = Router()

@router.callback_query(F.data == 'remove_admin_list_data')
async def remove_admin_func(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('👀Введите ID пользователь, которого хотите удалить', reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(AdminState.remove_admin)


@router.message(AdminState.remove_admin)
async def remove_admin_func(message: Message, state: FSMContext):
    telegram_id = message.text
    try:
        # Администратор успешно удален из базы данных.
        if await remove_admin(int(telegram_id)):
            await message.answer(f'✅Пользователь с ID {telegram_id} был удален!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

        else:
            await message.answer(f'⚠️Предупреждение, не удалось найти администратора для удаления!')

    except ValueError as e:
        await message.answer(f'❌Ошибка удаления пользователя. Ошибка: {e}', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

    await state.clear()