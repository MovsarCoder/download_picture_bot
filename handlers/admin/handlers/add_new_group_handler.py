from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from States.state import AdminState
from keyboard.keyboard_builder import make_row_inline_keyboards
from keyboard.keyboard import back_keyboard, admin_panel_keyboard
from database.crud import add_group

router = Router()


@router.callback_query(F.data == 'add_new_group_username_data')
async def add_new_group_username_db(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Отправьте username канала/группы (без использования @)!',
                                  reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(AdminState.add_new_group_username)


@router.message(AdminState.add_new_group_username)
async def fsm_add_new_group_username(message: Message, state: FSMContext):
    await message.answer(f'👀Хорошо! Username: {message.text}; Теперь отправьте название канала которое будет отображаться на кнопке!')
    await state.update_data(add_new_group_username=message.text)
    await state.set_state(AdminState.add_new_group_name)


@router.message(AdminState.add_new_group_name)
async def fsm_add_new_group_name(message: Message, state: FSMContext):
    await state.update_data(add_new_group_name=message.text)
    information_group = await state.get_data()

    # Сохраняем данные в JSON файл
    group_data = {
        'username': information_group['add_new_group_username'],
        'name': information_group['add_new_group_name']
    }

    # Если такая группа с таким Username присутствует, выводится данное сообщение.
    if not add_group(group_data):
        await message.answer(f'⚠️Группа с таким username уже существует: {group_data["username"]}', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
        return False

    # Если все успешно и Username свободен, группа успешно добавляется.
    await message.answer(f'✅Отлично! Информацию про новую группу:\nUsername: {group_data["username"]}\nName: {group_data["name"]}', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
    await state.clear()
