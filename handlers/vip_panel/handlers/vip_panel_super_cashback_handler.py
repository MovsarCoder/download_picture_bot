import os
import time
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from States.state import WildberriesCashback
from config.config import ADMIN
from keyboard.keyboard import super_feedbacks_show_keyboard, more_xlsx_super_product_keyboard, show_vip_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards
from handlers.vip_panel.functions.vip_panel_super_cashback_func import main

router = Router()


@router.callback_query(F.data == 'feedback_cashback_data_100')
async def feedback_cashback_data_100(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')

    await callback.message.answer('Выберите опцию: ', reply_markup=make_row_inline_keyboards(super_feedbacks_show_keyboard))


@router.callback_query(F.data == 'feedback_super_cashback_requests_data')
async def feedback_super_cashback_requests_data(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')

    await callback.message.answer('Введите название товара для поиска <b>Выгодного кешбэка</b>')
    await state.set_state(WildberriesCashback.get_name_super_cashback_product)


@router.message(WildberriesCashback.get_name_super_cashback_product)
async def feedback_super_cashback_requests_data_fsm(message: Message, state: FSMContext):
    await state.update_data(name_product=message.text)
    data = await state.get_data()
    name_product = data['name_product']

    send_name_box = await message.answer(f'Файл по запросу: <b>{name_product}</b> собирается. Ожидайте!')

    # Получаем администратора для бота
    admin = ADMIN

    start_time = time.time()
    await main(name_product)
    end_time = time.time()
    show_time = int(end_time - start_time)
    # Объединяем главную клавиатуру Vip Panel с клавиатурой на которой кнопка "Другой запрос"
    keyboard = show_vip_keyboard + more_xlsx_super_product_keyboard

    try:
        with open(f'../this_bot/{name_product}.csv', 'rb') as file:
            await message.bot.send_document(message.chat.id, BufferedInputFile(file.read(),
                                                                               filename=f'../this_bot/{name_product}.csv'),
                                            caption=f'✅ <b>Работа завершена успешно</b>\n'
                                                    f'<b>Затраченное время:</b> <i>{show_time} сек.</i>\n'
                                                    f'<b>Админ:</b> <i>{admin}</i>\n'
                                                    f'<b>Запрос:</b> "<i>{name_product}</i>"\n\n'
                                                    f'Вот ваш файл с данными.',
                                            reply_markup=make_row_inline_keyboards(keyboard))
        await send_name_box.delete()
        os.remove(f'../this_bot/{name_product}.csv')
        await state.clear()

    except Exception as ex:
        await send_name_box.delete()
        await message.answer(f'Запрос не обработан по причине: {ex}')
        os.remove(f'../this_bot/{name_product}.csv')

    print('Файл успешно отправлен.')


@router.callback_query(F.data == "more_new_xlsx_super_product_data")
async def more_new_xlsx_super_product_data(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await callback.message.answer('Введите название товара для поиска <b>Выгодного кешбэка</b>')
    await state.set_state(WildberriesCashback.get_name_super_cashback_product)
