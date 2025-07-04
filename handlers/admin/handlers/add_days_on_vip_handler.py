from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from States.state import AddDaysVipPanel
from keyboard.keyboard import back_keyboard, admin_panel_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards
from database.crud_sqlalchemy import add_days_on_player_vip_panel

router = Router()


@router.callback_query(F.data == 'add_days_on_vip_panel')
async def add_days_on_vip_player_function(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.answer('Введите пожалуйста Telegram ID чтобы распознать человека.', reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(AddDaysVipPanel.telegram_id)


@router.message(AddDaysVipPanel.telegram_id)
async def get_telegram_id_on_added_days(message: Message, state: FSMContext):
    telegram_id = message.text
    if telegram_id.isdigit():
        await state.update_data(telegram_id=telegram_id)
        await message.answer('🤝🏻 Успешно! Теперь введите пожалуйста количество дней, которое вы хотите добавить.', reply_markup=make_row_inline_keyboards(back_keyboard))
        await state.set_state(AddDaysVipPanel.get_days)

    else:
        await message.answer('❌ Ошибка! Введите пожалуйста корректный Telegram ID.', reply_markup=make_row_inline_keyboards(back_keyboard))
        await state.set_state(AddDaysVipPanel.telegram_id)
        return


@router.message(AddDaysVipPanel.get_days)
async def get_days_on_added_days(message: Message, state: FSMContext):
    added_days = message.text
    if added_days.isdigit():
        data = await state.get_data()
        telegram_id = data.get("telegram_id")

        if await add_days_on_player_vip_panel(telegram_id, int(added_days)):
            await message.answer(f'✅ Успешно! Вы добавили {added_days} дней пользователю в вип панель: {telegram_id}!',
                                 reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
        else:
            await message.answer(f'⚠️ Ошибка! Не смогли найти пользователя с {telegram_id=}! Введите правильный Telegram ID.', reply_markup=make_row_inline_keyboards(back_keyboard))
            await state.set_state(AddDaysVipPanel.telegram_id)
            return

    else:
        await message.answer('❌ Ошибка! Введите корректное число!', reply_markup=make_row_inline_keyboards(back_keyboard))
        await state.set_state(AddDaysVipPanel.get_days)
        return


    await state.clear()