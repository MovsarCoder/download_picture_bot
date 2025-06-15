from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.crud import get_chat_id
from States.state import NewsLetter
from keyboard.keyboard import back_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards

router = Router()


# Обработчик нажатия кнопки "broadcast_message"
@router.callback_query(F.data == "broadcast_message")
async def handle_broadcast_button(callback: CallbackQuery, state: FSMContext):
    # Переход в состояние ввода текста или медиа для рассылки
    await callback.answer()
    await callback.message.answer("Введите текст или отправьте медиа для рассылки:", reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(NewsLetter.text)


# Обработчик текстовых и медиа-сообщений в состоянии NewsLetter.text
@router.message(NewsLetter.text, F.content_type.in_({"text", "photo", "video", "document"}))
async def send_broadcast(message: Message, state: FSMContext):
    users = get_chat_id()

    success = 0
    failed = 0

    await message.answer(f"Количество пользователей для рассылки: {len(users)}")
    for user in users:
        print(f"Отправка сообщения пользователю с chat_id: {user}")
        try:
            # Определяем тип контента
            if message.text:
                # Рассылка текста
                await message.bot.send_message(chat_id=str(user), text=message.text)
            elif message.photo:
                # Рассылка фото
                await message.bot.send_photo(
                    chat_id=str(user),
                    photo=message.photo[-1].file_id,
                    caption=message.caption if message.caption else None
                )
            elif message.video:
                # Рассылка видео
                await message.bot.send_video(
                    chat_id=str(user),
                    video=message.video.file_id,
                    caption=message.caption if message.caption else None
                )
            elif message.document:
                # Рассылка документа
                await message.bot.send_document(
                    chat_id=str(user),
                    document=message.document.file_id,
                    caption=message.caption if message.caption else None
                )
            else:
                failed += 1
                continue

            success += 1
        except Exception as e:
            await message.answer(f"Не удалось отправить сообщение пользователю {user}: {e}")
            failed += 1

    # Отправляем итог админу
    await message.answer(f"Рассылка завершена.\nУспешно: {success}\nНеудачно: {failed}")

    # Завершаем состояние
    await state.clear()
