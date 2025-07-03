from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboard.keyboard import back_keyboard, admin_panel_keyboard, names_vip_panel, keyboard_main_admin
from keyboard.keyboard_builder import make_row_inline_keyboards, make_row_keyboards
from database.crud_sqlalchemy import add_new_user_vip_panel
from States.state import AddedVipPanel

router = Router()


@router.callback_query(F.data == 'add_new_user_vip_panel')
async def new_user_vip_panel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите Телеграмм ID для добавления: ', reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(AddedVipPanel.get_id)


@router.message(AddedVipPanel.get_id)
async def get_telegram_id_vip_panel(message: Message, state: FSMContext):
    telegram_id_user = message.text
    if not telegram_id_user.isdigit():
        await message.answer(f'❌ Ошибка! Введите корректный TelegramID!')
        await state.set_state(AddedVipPanel.get_id)
        return

    await state.update_data(add_vip_panel_id=telegram_id_user)
    await message.answer('Отлично! Теперь введите Имя и Фамилия: ')
    await state.set_state(AddedVipPanel.get_name)


@router.message(AddedVipPanel.get_name)
async def get_name_vip_panel(message: Message, state: FSMContext):
    await state.update_data(add_vip_panel_name=message.text)
    await message.answer("Отлично! Теперь введите количество дней, которые вы хотите выдать")
    await state.set_state(AddedVipPanel.number_of_days)


@router.message(AddedVipPanel.number_of_days)
async def get_days_of_vip_panel(message: Message, state: FSMContext):
    number_of_days = message.text

    if not number_of_days.isdigit():
        await message.answer(f'❌ Ошибка! Введите целое число!')
        await state.set_state(AddedVipPanel.number_of_days)
        return

    await state.update_data(number_of_days_vip_panel=number_of_days)
    await message.answer("Отлично! Теперь введите название вип категории (Стандарт| Стандарт + | Премиум)", reply_markup=make_row_keyboards(names_vip_panel))
    await state.set_state(AddedVipPanel.status_vip)


@router.message(AddedVipPanel.status_vip, F.text.in_(['Стандарт', 'Стандарт +', 'Премиум']))
async def get_status_vip_name(message: Message, state: FSMContext):
    name_vip = message.text
    data = await state.get_data()

    vip_panel_information = {
        'telegram_id': data['add_vip_panel_id'],
        'name': data['add_vip_panel_name'],
        "number_of_days": data['number_of_days_vip_panel'],
        "vip_status": name_vip
    }

    if await add_new_user_vip_panel(vip_panel_information):
        await message.answer(f'✅Пользователь успешно был добавлен в Vip!', reply_markup=make_row_keyboards(keyboard_main_admin))
        await message.answer(f'Информация пользователя: {vip_panel_information}', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
    else:
        await message.answer('⚠️Такой пользователь уже существует в базе данных!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

    await state.clear()
