import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tg_bot.config import load_config
from tg_bot.handlers import register_handlers, register_payment_handlers, register_admin_handlers
storage = MemoryStorage()
logger = logging.getLogger(__name__)

def register_all_handlers(dp):
    register_handlers(dp)
    register_payment_handlers(dp)
    register_admin_handlers(dp)

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config('.env')
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot)
    dp.storage = storage
    bot['config'] = config
    register_all_handlers(dp)
    while True:
        try:
            await dp.start_polling()
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    asyncio.run(main())