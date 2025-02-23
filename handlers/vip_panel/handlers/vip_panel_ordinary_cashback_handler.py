import os
import time
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from States.state import WildberriesCashback
from config.config import ADMIN
from keyboard.keyboard import more_xlsx_product_keyboard, show_vip_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards
from handlers.vip_panel.functions.vip_panel_ordinary_cashback_func import main

router = Router()


@router.callback_query(F.data == 'feedback_cashback_data')
async def send_name_product_func(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')

    await callback.message.answer("Запущен парсер кэшбека Wildberries по поисковому запросу или категории! Вставьте ссылку на категорию или напишите запрос. Например: ```https://www.wildberries.ru/catalog/dlya-doma/predmety-interera/svechi-i-podsvechniki``` Или ```Платье женское``` ",
                                  parse_mode=ParseMode.MARKDOWN)

    await state.set_state(WildberriesCashback.get_name_product)


@router.message(WildberriesCashback.get_name_product)
async def get_name_product_func(message: Message, state: FSMContext):
    await state.update_data(name_product=message.text)
    data = await state.get_data()

    await message.answer(f'⚙️ Парсер начал работу...')

    # Запуск парсера
    name_product = data['name_product'] # Получаем введеный запрос пользователя

    # Получаем администратора для бота
    admin = ADMIN
    start_time = time.time()
    await main(name_product)
    end_time = time.time()
    show_time = int(end_time - start_time)

    # Объединяем главную клавиатуру Vip Panel с клавиатурой на которой кнопка "Другой запрос"
    keyboard = show_vip_keyboard + more_xlsx_product_keyboard

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

        os.remove(f'../this_bot/{name_product}.csv')
        await state.clear()

    except Exception as ex:
        await message.answer(f'Запрос не обработан по причине: {ex}')
        os.remove(f'../this_bot/{name_product}.csv')

    print('Файл успешно отправлен.')


@router.callback_query(F.data == 'more_new_xlsx_ordinary_product_data')
async def more_new_xlsx_func(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.answer(
        "Запущен парсер кэшбека Wildberries по поисковому запросу или категории! Вставьте ссылку на категорию или напишите запрос. Например: ```https://www.wildberries.ru/catalog/dlya-doma/predmety-interera/svechi-i-podsvechniki``` Или ```Платье женское``` ",
        parse_mode=ParseMode.MARKDOWN)

    await state.set_state(WildberriesCashback.get_name_product)
