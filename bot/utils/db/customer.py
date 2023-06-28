import aiohttp
from aiogram.types import CallbackQuery, Message
from uuid import UUID


async def create_user(event: CallbackQuery | Message, customer_class: UUID):
    async with aiohttp.ClientSession() as session:
        url = "http://repetitor_backend/api/v1/customer"
        data = {
            "tlg_user_id": event.from_user.id,
            "customer_class": customer_class,
            "tlg_language": event.from_user.language_code,
            "tlg_first_name": event.from_user.first_name,
            "tlg_user_name": event.from_user.username,
            "tlg_last_name": event.from_user.last_name,
        }
        async with session.post(url, json=data) as response:
            print(response.status)
            print(await response.json())
            id_resp = await response.json()
            return id_resp


async def get_user(tlg_user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://repetitor_backend/api/v1/customer/{tlg_user_id}"
        ) as response:
            val = await response.json()
            return val
