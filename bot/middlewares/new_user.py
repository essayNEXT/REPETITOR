from typing import Callable, Dict, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

# Для проверки работы кода (начало)
base = [548019148,]
def is_new_user(message: Message) -> bool:
    return message.from_user.id in base

def create_new_user():
    return "Новый пользователь"

# Для проверки работы кода (конец)


class NewUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str,Any],
    ) -> Any:
        if is_new_user(event):
            return await handler(event, data)
        await event.answer(f"{create_new_user()}") # Вставить функцию создания пользователя





