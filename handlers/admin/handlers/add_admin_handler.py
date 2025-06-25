from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboard.keyboard import back_keyboard, admin_panel_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards
from States.state import AdminState
from database.crud_sqlalchemy import add_admin

router = Router()


@router.callback_query(F.data == 'new_admin_data')
async def new_admin_user_func(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('👀Введите ID пользователя, которого хотите добавить как админ', reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(AdminState.new_admin)


@router.message(AdminState.new_admin)
async def add_admin_id(message: Message, state: FSMContext):
    telegram_id = message.text
    try:
        if await add_admin(int(telegram_id)):
            # Добавляем ID пользователя в список администраторов
            await message.answer(f'✅Пользователь с ID {telegram_id} добавлен как админ.', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
        else:
            # Есть такой администратор существует в базе данных!
            await message.answer(f'⚠️Предупреждение, администратор уже существует!')

    except ValueError as e:
        await message.answer(f'❌Ошибка добавления пользователя. Ошибка: {e}', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

    await state.clear()