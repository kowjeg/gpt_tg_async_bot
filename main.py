import logging
import asyncio
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from handlers import router





async def main():
    logger = logging.getLogger(__name__)
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())