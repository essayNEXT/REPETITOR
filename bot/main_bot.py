import asyncio
import logging
from middlewares import first_contact
from handlers import (
    translate,
    inline_kb_test,
    first_contact_handler,
    customer_context_handler,
)
from utils.commands import set_commands
from create_bot import bot, dp


async def main():
    file_log = logging.FileHandler("log/bot.log")
    console_out = logging.StreamHandler()
    logging.basicConfig(
        handlers=(file_log, console_out),
        level=logging.INFO,
        datefmt="%m.%d.%Y %H:%M:%S",
        format="[%(asctime)s | %(levelname)s]: %(message)s",
    )
    dp.message.outer_middleware(first_contact.FirstContactMiddleware())
    await set_commands(bot)
    dp.include_router(first_contact_handler.router)
    dp.include_router(customer_context_handler.router)
    dp.include_router(inline_kb_test.router)
    dp.include_router(translate.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
