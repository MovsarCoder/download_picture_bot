import os
import time
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from States.state import WildberriesCashback
from keyboard.keyboard import more_xlsx_product_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards
from handlers.vip_panel.vip_panel_functions.vip_panel_ordinary_cashback_func import main

router = Router()


@router.callback_query(F.data == 'feedback_cashback_data')
async def send_name_product_func(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')

    await callback.message.answer('Введите название товара для поиска кэшбэка: ')
    await state.set_state(WildberriesCashback.get_name_product)


@router.message(WildberriesCashback.get_name_product)
async def get_name_product_func(message: Message, state: FSMContext):
    await state.update_data(name_product=message.text)
    data = await state.get_data()
    name_product = data['name_product']

    send_name_box = await message.answer(f'Файл по запросу: {name_product} собирается. Ожидайте!')

    start_time = time.time()
    await main(name_product)
    end_time = time.time()
    show_time = int(end_time - start_time)

    try:
        with open(f'../this_bot/{name_product}.xlsx', 'rb') as file:
            await message.bot.send_document(message.chat.id, BufferedInputFile(file.read(),
                                                                                    filename=f'../this_bot/{name_product}.xlsx'),
                                                 caption=f'✅ Работа завершена успешно\n'
                                                         f'Затраченное время: {show_time} сек.\n'
                                                         f'Админ: @timaadev\nЗапрос: "{name_product}"'
                                                         f'\n\nВот ваш файл с данными.',
                                                 reply_markup=make_row_inline_keyboards(more_xlsx_product_keyboard))
        await send_name_box.delete()
        os.remove(f'../this_bot/{name_product}.xlsx')
        await state.clear()

    except Exception as ex:
        await send_name_box.delete()
        await message.answer(f'Запрос не обработан по причине: {ex}')
        os.remove(f'../this_bot/{name_product}.xlsx')

    print('Файл успешно отправлен.')


@router.callback_query(F.data == 'more_new_xlsx_ordinary_product_data')
async def more_new_xlsx_func(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Введите название товара для поиска кешбека: ')
    await state.set_state(WildberriesCashback.get_name_product)
