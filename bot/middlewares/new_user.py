from typing import Callable, Dict, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
import aiohttp


async def get_user_id(message: Message) -> int:
    user_id = message.from_user.id
    return user_id


async def is_new_user(user_id) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://repetitor_backend/api/v1/customer/{user_id}"
        ) as response:
            val = await response.json()
            for item in val:
                val_id = item["id"]
                val_active = item["is_active"]
                if val_id == user_id and val_active is True:
                    return True
                else:
                    return False


class NewUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = await get_user_id(message=event)
        if await is_new_user(user_id):
            return await handler(event, data)
        await event.answer(f"Новый пользователь {user_id} {await is_new_user(user_id)}")
