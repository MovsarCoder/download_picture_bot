from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from handlers.download_puctire_and_video.download_video_wb.download_video_functions.download_video_func import construct_host_v2
from keyboard.keyboard import more_keyboard_video
import requests
from States.state import *
from keyboard.keyboard_builder import make_row_inline_keyboards

router = Router()


@router.callback_query(F.data == 'download_video_data')
async def send_download_video_data(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Отправьте ссылку или артикул товара')
    await state.set_state(Wildberries.download_video)


@router.message(Wildberries.download_video)
async def fsm_send_download_video(message: Message, state: FSMContext):
    message_sabr = await message.answer('Ожидайте! Скачивание выполняется..')
    message_url_or_feedback = message.text

    func_return_url_video = construct_host_v2(message_url_or_feedback, "video")

    if not func_return_url_video:
        await message_sabr.delete()
        await message.answer('Ошибка: Неверный ID или тип видео.', reply_markup=make_row_inline_keyboards(more_keyboard_video))
        return

    try:
        response = requests.head(func_return_url_video)  # Используем HEAD-запрос для проверки доступности
        response.raise_for_status()  # Вызывает исключение для статусов 4xx и 5xx

        await message_sabr.delete()
        await message.bot.send_video(message.chat.id, video=func_return_url_video, caption='✅ Готово', reply_markup=make_row_inline_keyboards(more_keyboard_video))
        await state.clear()

    except requests.HTTPError:
        await message_sabr.delete()
        await message.answer('Произошла ошибка! Возможно на товаре отсутствует видео или неверная ссылка.', reply_markup=make_row_inline_keyboards(more_keyboard_video))
    except requests.RequestException as req_err:
        await message_sabr.delete()
        await message.answer(f'Сетевая ошибка: {req_err}')
    except Exception as e:
        await message_sabr.delete()
        await message.answer(f'Неизвестная ошибка: {e}')


@router.callback_query(F.data == 'more_download_video')
async def more_download(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Wildberries.download_video)
    await callback.answer('More downloading :///')
    await callback.message.answer('Продолжим! Отправьте ссылку или артикул товара.')
