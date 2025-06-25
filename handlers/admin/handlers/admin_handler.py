from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboard.keyboard_builder import make_row_inline_keyboards
from keyboard.keyboard import *
from database.crud_sqlalchemy import get_admin_list

router = Router()


@router.message(Command('admin_panel'))
@router.message(F.text == '⚙️ Управление ботом')
async def cmd_admin(callback_or_message: CallbackQuery | Message, state: FSMContext):
    admin_users_list = await get_admin_list()

    if callback_or_message.from_user.id in admin_users_list:
        if isinstance(callback_or_message, CallbackQuery):
            await callback_or_message.message.answer('❕Выберите действие', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

        elif isinstance(callback_or_message, Message):
            await callback_or_message.answer('❕Выберите действие', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

    else:
        await callback_or_message.answer(
            f'⚠️{callback_or_message.from_user.full_name}({callback_or_message.from_user.id}) вы не можете получить доступ к Admin функциям данного бота! Так как не являетесь Admin!')

    await state.clear()


@router.callback_query(F.data == 'back_data2')
async def back_func_2(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('❕Выберите действие', show_alert=True, reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
    await state.clear()

#
# @router.callback_query(F.data == 'back_data')
# async def back_func(callback: CallbackQuery, state: FSMContext):
#     await state.clear()
#     await callback.message.answer('❕Выберите действие', show_alert=True, reply_markup=make_row_inline_keyboards(keyboard_main_admin))
