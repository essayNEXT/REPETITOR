import asyncio
import logging
from handlers import echo
from create_bot import bot, dp


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(echo.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
