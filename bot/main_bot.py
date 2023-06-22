import asyncio
import logging
from middlewares import new_user
from handlers import echo, inline_kb_test
from utils.commands import set_commands
from create_bot import bot, dp


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.message.middleware(new_user.NewUserMiddleware())
    await set_commands(bot)
    dp.include_router(inline_kb_test.router)
    dp.include_router(echo.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
