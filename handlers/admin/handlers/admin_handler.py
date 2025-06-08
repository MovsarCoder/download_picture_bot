from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from keyboard.keyboard import *
from States.state import *
from database.crud import *
from keyboard.keyboard_builder import make_row_inline_keyboards

router = Router()


@router.message(Command('admin_panel'))
@router.message(F.text == '⚙️ Управление ботом')
async def cmd_admin(callback_or_message: CallbackQuery | Message, state: FSMContext):
    await state.clear()
    admin_users_list = get_admin_list()
    if callback_or_message.from_user.id in admin_users_list:
        if isinstance(callback_or_message, CallbackQuery):
            await callback_or_message.message.answer('❕Выберите действие', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
        elif isinstance(callback_or_message, Message):
            await callback_or_message.answer('❕Выберите действие', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

    else:
        await callback_or_message.answer(
            f'⚠️{callback_or_message.from_user.full_name}({callback_or_message.from_user.id}) вы не можете получить доступ к Admin функциям данного бота! Так как не являетесь Admin!')


@router.callback_query(F.data == 'new_admin_data')
async def new_admin_user_func(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('👀Введите ID пользователя, которого хотите добавить как админ', reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(AdminState.new_admin)


@router.message(AdminState.new_admin)
async def add_admin_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    try:
        # Добавляем ID пользователя в список администраторов
        if add_admin(message.text):
            await message.answer(f'✅Пользователь с ID {message.text} добавлен как админ.', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
            await state.clear()
    # Есть такой администратор существует в базе данных!
    except Exception as e:
        await message.answer(f'❌Ошибка добавления пользователя. Ошибка: {e}', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))


@router.callback_query(F.data == 'remove_admin_list_data')
async def remove_admin_func(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('👀Введите ID пользователь, которого хотите удалить', reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(AdminState.remove_admin)


@router.message(AdminState.remove_admin)
async def remove_admin_func(message: Message, state: FSMContext):
    try:
        remove_admin(message.text)
        # Администратор успешно удален из базы данных.
        await message.answer(f'✅Пользователь с ID {message.text} был удален!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
        await state.clear()
    except ValueError as e:
        await message.answer(f'❌Ошибка удаления пользователя. Ошибка: {e}', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))


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


@router.callback_query(F.data == 'delete_group_data')
async def remove_group_db_func(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text('Send username in the remove group/chanel (dont use "@")',
                                     reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(AdminState.delete_group)


@router.message(AdminState.delete_group)
async def fsm_remove_group_db(message: Message, state: FSMContext):
    try:
        # Переменная для ловли сообщения от пользователя
        message_text = message.text
        # Если с написанным пользователем Username присутствует, то она удалится.
        remove_func = remove_group(message_text)
        # Если функция remove_func возвращает True - группа удаляется и выводится сообщение
        if remove_func:
            await message.answer(f'✅Группа с Username: {message_text} успешно удалена!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
            await state.clear()
        # Если такой группы нет.
        else:
            await message.answer('⚠️Невозможно найти группу с таким Username!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

    except KeyError as e:
        await message.answer(f'❌Ошибка типа 3453-234567 - {e}!')


@router.callback_query(F.data == 'list_group_data')
async def group_list_db(callback: CallbackQuery):
    await callback.answer('')
    groups = load_groups()
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
        await state.clear()

    else:
        await message.answer('⚠️Такой пользователь уже существует в базе данных!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
        await state.clear()
        
        
@router.callback_query(F.data == 'delete_user_with_vip_panel')
async def delete_user_vip_panel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите ID пользователя:')
    await state.set_state(DeleteVipPanel.get_id)


@router.message(DeleteVipPanel.get_id)
async def delete_user_vip_panel_fsm(message: Message, state: FSMContext):
    user_get_text = message.text
    user_name = ''

    data = {
        'telegram_id': user_get_text,
        'name': user_name
    }

    if delete_users_with_vip_panel_functions(data):
        await message.answer('✅Человек успешно удален из списка Vip пользователей!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
        await state.clear()
    else:
        await message.answer('⚠️Такого пользователя нет в списке Vip пользователей!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))
        await state.clear()

@router.callback_query(F.data == 'back_data2')
async def back_func_2(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('❕Выберите действие', show_alert=True, reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

#
# @router.callback_query(F.data == 'back_data')
# async def back_func(callback: CallbackQuery, state: FSMContext):
#     await state.clear()
#     await callback.message.answer('❕Выберите действие', show_alert=True, reply_markup=make_row_inline_keyboards(keyboard_main_admin))
