from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboard.keyboard import show_vip_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards

router = Router()

@router.callback_query(F.data == 'vip_data')
async def show_vip_keyboard_func(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите нужную функцию:', reply_markup=make_row_inline_keyboards(show_vip_keyboard))


@router.callback_query(F.data == 'more_stop_vip_panel')
async def more_send_stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Выберите функцию', reply_markup=make_row_inline_keyboards(show_vip_keyboard))
