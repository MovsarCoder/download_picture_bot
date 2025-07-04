from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.crud_sqlalchemy import remove_days_on_player_vip_panel
from keyboard.keyboard import back_keyboard, admin_panel_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards
from States.state import RemoveDaysVipPanel

router = Router()


@router.callback_query(F.data == 'remove_days_on_vip_panel')
async def remove_days_on_vip_player_function(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.answer('Введите пожалуйста Telegram ID чтобы распознать человека.', reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(RemoveDaysVipPanel.telegram_id)


@router.message(RemoveDaysVipPanel.telegram_id)
async def get_telegram_id_on_remove_days(message: Message, state: FSMContext):
    telegram_id = message.text
    if telegram_id.isdigit():
        await state.update_data(telegram_id=telegram_id)
        await message.answer('🤝🏻 Успешно! Теперь введите количество дней которые вы хотите забрать у пользователя.', reply_markup=make_row_inline_keyboards(back_keyboard))
        await state.set_state(RemoveDaysVipPanel.get_days)


    else:
        await message.answer('❌ Ошибка! Введите корректный Telegram ID.', reply_markup=make_row_inline_keyboards(back_keyboard))
        await state.set_state(RemoveDaysVipPanel.telegram_id)
        return


@router.message(RemoveDaysVipPanel.get_days)
async def get_days_on_remove_days(message: Message, state: FSMContext):
    removed_days = message.text

    if removed_days.isdigit():
        data = await state.get_data()
        telegram_id = data.get("telegram_id")

        if await remove_days_on_player_vip_panel(telegram_id, int(removed_days)):
            await message.answer(f'✅ Успешно! Вы забрали {removed_days=} у {telegram_id=}.',
                                 reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

        else:
            await message.answer(f'⚠️ Ошибка! Не смогли найти пользователя с {telegram_id=}! Введите правильный Telegram ID.', reply_markup=make_row_inline_keyboards(back_keyboard))
            await state.set_state(RemoveDaysVipPanel.telegram_id)
            return

    else:
        await message.answer('❌ Ошибка! Не корректное число.', reply_markup=make_row_inline_keyboards(back_keyboard))
        await state.set_state(RemoveDaysVipPanel.get_days)
        return

    await state.clear()
