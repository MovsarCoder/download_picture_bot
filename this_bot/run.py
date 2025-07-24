import asyncio
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook
from config.settings import TOKEN
from aiogram import Bot, Dispatcher
from handlers import router

from shedular_start import start_scheduler


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await bot(DeleteWebhook(drop_pending_updates=True))

    # Запуск Scheduler
    start_scheduler()

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
