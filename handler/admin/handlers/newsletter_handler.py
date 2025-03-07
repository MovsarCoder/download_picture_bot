from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from States.state import *
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

router = Router()

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)


# Инициализация базы данных
DATABASE_URL = "sqlite:///bot.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Модель пользователя
class User(Base):
    __tablename__ = "users"  # Исправлено на __tablename__
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String, unique=True, nullable=False)


# Обработчик текстовых и медиа-сообщений в состоянии Letter.text
@router.message(NewsLetter.text, F.content_type.in_({"text", "photo", "video", "document"}))
async def send_broadcast(message: Message, state: FSMContext):
    session = SessionLocal()
    users = session.query(User).all()
    print(users)

    success = 0
    failed = 0

    print(f"Количество пользователей для рассылки: {len(users)}")
    for user in users:
        print(user)
        print(f"Отправка сообщения пользователю с chat_id: {user.chat_id}")
        try:
            # Определяем тип контента
            if message.text:
                # Рассылка текста
                await message.bot.send_message(chat_id=str(user.chat_id), text=message.text)
            elif message.photo:
                # Рассылка фото
                await message.bot.send_photo(
                    chat_id=str(user.chat_id),
                    photo=message.photo[-1].file_id,
                    caption=message.caption if message.caption else None
                )
            elif message.video:
                # Рассылка видео
                await message.bot.send_video(
                    chat_id=str(user.chat_id),
                    video=message.video.file_id,
                    caption=message.caption if message.caption else None
                )
            elif message.document:
                # Рассылка документа
                await message.bot.send_document(
                    chat_id=str(user.chat_id),
                    document=message.document.file_id,
                    caption=message.caption if message.caption else None
                )
            else:
                failed += 1
                continue

            success += 1
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user.chat_id}: {e}")
            failed += 1

    # Отправляем итог админу
    await message.answer(f"Рассылка завершена.\nУспешно: {success}\nНеудачно: {failed}")

    # Завершаем состояние
    await state.clear()
    session.close()


# Обработчик нажатия кнопки "broadcast_message"
@router.callback_query(F.data == "broadcast_message")
async def handle_broadcast_button(callback_query: CallbackQuery, state: FSMContext):
    # Переход в состояние ввода текста или медиа для рассылки
    await callback_query.message.answer("Введите текст или отправьте медиа для рассылки:")
    await state.set_state(NewsLetter.text)
    await callback_query.answer()
