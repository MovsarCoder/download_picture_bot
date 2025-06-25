from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboard.keyboard_builder import make_row_inline_keyboards
from keyboard.keyboard import admin_panel_keyboard
from database.crud_sqlalchemy import load_groups

router = Router()


@router.callback_query(F.data == 'list_group_data')
async def group_list_db(callback: CallbackQuery):
    await callback.answer('')
    groups = await load_groups()
    keyboard = []

    # если в JSON-файле нет никаких групп для подписки, выведется данное сообщение
    if not groups:
        await callback.message.answer("⚠️Нет добавленных групп.", reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
        return
    # если в JSON-файле есть группа из нее создастся клавиатура
    for group in groups:
        keyboard.append([InlineKeyboardButton(text=f'{group["name"]}', url=f'https://t.me/{group["username"]}')])

    # добавление кнопки "Назад" к клавиатуре чтобы вернутся к списку функций администратора.
    keyboard.append([InlineKeyboardButton(text='🔙Назад', callback_data='back_data2')])
    keyboard_list = InlineKeyboardMarkup(inline_keyboard=keyboard)

    # вывод сообщения со всеми группами и кнопкой "Назад"
    await callback.message.edit_text('📋Доступные группы:', reply_markup=keyboard_list)
