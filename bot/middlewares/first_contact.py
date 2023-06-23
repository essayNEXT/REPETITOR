from typing import Callable, Dict, Awaitable, Any
from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiohttp


async def get_user_id(message: Message) -> int:
    user_id = message.from_user.id
    return user_id


async def is_existing_user(tlg_user_id) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://repetitor_backend/api/v1/customer/{tlg_user_id}"
        ) as response:
            val = await response.json()
            for item in val:
                val_id = item["tlg_user_id"]
                val_active = item["is_active"]
                if val_id == tlg_user_id and val_active is True:
                    return True
                else:
                    return False


class FirstContactMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = await get_user_id(message=event)
        if await is_existing_user(user_id):
            return await handler(event, data)

        # Якщо користувача немає в базі даних, то опрацювання переривається. Пропонується реєстрація
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="Зареєструватись", callback_data="registration"
            )
        )

        await event.answer(
            f"Привіт, {event.from_user.full_name}!\n"
            "Щоб скористатись моїми послугами потрібно зареєструватись.\n",
            reply_markup=builder.as_markup(),
        )
        return
