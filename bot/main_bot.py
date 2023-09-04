import asyncio
import logging
from middlewares import first_contact
from handlers import (
    translate_handler,
    first_contact_handler,
    customer_context_handler,
)
from utils.commands import set_commands
from utils.help import HelpPublisher
from create_bot import bot, dp

from keyboards.user_context.user_context_kb import ChooseContextKeyboard
from keyboards.native_language.native_language_kb import ChooseNativeLanguageKeyboard
from keyboards.first_contact.first_contact_kb import (
    ConfirmKeyboard,
    ChangeUserDataKeyboard,
)

kb_classes = [
    ConfirmKeyboard,
    ChangeUserDataKeyboard,
    ChooseContextKeyboard,
    ChooseNativeLanguageKeyboard,
]


async def help_create():
    try:
        await HelpPublisher(kb_classes)
    except Exception:
        print("Table do not exist. Do migrations before.")


async def main():
    # file_log = logging.FileHandler("log/bot.log")
    # console_out = logging.StreamHandler()
    # logging.basicConfig(
    #     handlers=(file_log, console_out),
    #     level=logging.INFO,
    #     datefmt="%m.%d.%Y %H:%M:%S",
    #     format="[%(asctime)s | %(levelname)s]: %(message)s",
    # )
    dp.message.outer_middleware(first_contact.FirstContactMiddleware())
    await set_commands(bot)
    dp.include_router(first_contact_handler.router)
    dp.include_router(customer_context_handler.router)
    dp.include_router(translate_handler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(help_create())
    asyncio.run(main())
