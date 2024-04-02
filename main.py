import asyncio
import logging
from aiogram import Dispatcher
from utils import dp
from utils import bot
from utils import db
import handlers


async def main(dp: Dispatcher):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(name)s'
                                                   '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    db.CreateTables()

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main(dp))
