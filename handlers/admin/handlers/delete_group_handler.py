from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from States.state import AdminState
from database.crud import remove_group
from keyboard.keyboard_builder import make_row_inline_keyboards
from keyboard.keyboard import back_keyboard, admin_panel_keyboard

router = Router()


@router.callback_query(F.data == 'delete_group_data')
async def remove_group_db_func(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Send username in the remove group/chanel (dont use "@")',
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
        # Если такой группы нет.
        else:
            await message.answer('⚠️Невозможно найти группу с таким Username!', reply_markup=make_row_inline_keyboards(admin_panel_keyboard))

    except KeyError as e:
        await message.answer(f'❌Ошибка типа 3453-234567 - {e}!')

    await state.clear()
