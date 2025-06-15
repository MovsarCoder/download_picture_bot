from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboard.keyboard import back_keyboard, admin_panel_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards
from database.crud import add_new_user_vip_panel
from States.state import AddedVipPanel

router = Router()


@router.callback_query(F.data == 'add_new_user_vip_panel')
async def new_user_vip_panel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите Телеграмм ID для добавления: ', reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(AddedVipPanel.get_id)


@router.message(AddedVipPanel.get_id)
async def get_telegram_id_vip_panel(message: Message, state: FSMContext):
    await state.update_data(add_vip_panel_id=message.text)
    await message.answer('Отлично! Теперь введите Имя и Фамилия: ')
    await state.set_state(AddedVipPanel.get_name)


@router.message(AddedVipPanel.get_name)
async def get_name_vip_panel(message: Message, state: FSMContext):
    await state.update_data(add_vip_panel_name=message.text)
    data = await state.get_data()
    vip_panel_information = {
        'telegram_id': data['add_vip_panel_id'],
        'name': data['add_vip_panel_name']
    }

    if add_new_user_vip_panel(vip_panel_information):
        await message.answer('✅Пользователь успешно был добавлен!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

    else:
        await message.answer('⚠️Такой пользователь уже существует в базе данных!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

    await state.clear()
