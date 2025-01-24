from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from handlers.download_puctire_and_video.download_picture_wb.download_picture_func import get_product_info
from keyboard.keyboard import more_keyboard
from aiogram import F, Router
import asyncio
from States.state import *
from keyboard.keyboard_builder import make_row_inline_keyboards

router = Router()


@router.callback_query(F.data == 'download_picture_data')
async def download_picture_func(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Отправьте ссылку или артикул товара')
    await state.set_state(Wildberries.download_picture)


@router.message(Wildberries.download_picture)
async def download_picture_func_fsm(message: Message, state: FSMContext):
    waiting_message = await message.answer('Ожидайте! Ваш запрос выполняется...')
    url = message.text
    # Получаем информацию о продукте
    result = get_product_info(url)

    # Проверяем, вернула ли функция корректные данные
    if not result:
        await waiting_message.delete()
        await message.answer('Не удалось получить информацию о товаре. Необходимо отправить ссылку без текстового описания.')
        return

    # Распаковка данных
    name_product, old_price, new_price, brand, item_goods, rating_goods, url_photo, feedbacks, desc = result

    # await state.update_data(download_picture_func=url)
    url_photo_split = [i for i in url_photo.split('\n') if i]  # Убираем пустые строки
    media = []

    try:
        await asyncio.sleep(5)
        await waiting_message.delete()

        for i in url_photo_split:
            # media.append(InputMediaPhoto(media=i, caption=f'Готово! ✅\n\n'
            #                                               f'<b>Название товара:</b> <i>{name_product}</i>\n'
            #                                               f'<b>Артикул товара:</b> <i>{item_goods}</i>\n'
            #                                               f'<b>Цена со скидкой:</b> <i>{int(new_price)} ₽</i>\n'
            #                                               f'<b>Цена без скидки:</b> <i>{int(old_price)} ₽</i>\n'
            #                                               f'<b>Рейтинг товара:</b> <i>{rating_goods}</i>\n'
            #                                               f'<b>Название бренда:</b> <i>{brand}</i>\n'
            #                                               f'<b>Ссылка на товар:</b> <i>{message.text}</i>\n'
            #                                               f'<b>Отзывы:</b> <i>{feedbacks}</i>'))

            media.append(InputMediaPhoto(media=i))

        await message.bot.send_media_group(chat_id=message.from_user.id, media=media)
        await message.bot.send_message(chat_id=message.from_user.id, text=f'Готово! ✅\n\n'
                                                                          f'<b>Название товара:</b> <i>{name_product}</i>\n'
                                                                          f'<b>Артикул товара:</b> <i>{item_goods}</i>\n'
                                                                          f'<b>Цена со скидкой:</b> <i>{int(new_price)} ₽</i>\n'
                                                                          f'<b>Цена без скидки:</b> <i>{int(old_price)} ₽</i>\n'
                                                                          f'<b>Рейтинг товара:</b> <i>{rating_goods}</i>\n'
                                                                          f'<b>Название бренда:</b> <i>{brand}</i>\n'
                                                                          f'<b>Ссылка на товар:</b> <i>{message.text}</i>\n'
                                                                          f'<b>Отзывы:</b> <i>{feedbacks}</i>\n\n'
                                                                          f'<b>Описание:</b> <i>{desc}</i>',
                                       reply_markup=make_row_inline_keyboards(more_keyboard), disable_web_page_preview=True)
        await state.clear()

    except Exception as e:
        await message.answer(f'Ошибка: {e}! Проверьте валидность ссылки или что-то!')


@router.callback_query(F.data == 'more_download_picture')
async def more_download(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Wildberries.download_picture)
    await callback.answer('More downloading :///')
    await callback.message.answer('Продолжим скачивание! Отправьте ссылку или артикул товара.')
