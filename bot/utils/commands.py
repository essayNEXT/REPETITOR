from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="help",
            description="Виводить повідомлення з допомогою відповідно поточного стану",
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
