import aiohttp
from aiogram.types import CallbackQuery, Message
from uuid import UUID


async def create_user(event: CallbackQuery | Message, customer_type: UUID):
    async with aiohttp.ClientSession() as session:
        url = "http://repetitor_backend/api/v1/customer"
        data = {
            "tlg_user_id": event.from_user.id,
            "customer_type": customer_type,
            "tlg_language": event.from_user.language_code,
            "tlg_first_name": event.from_user.first_name,
            "tlg_user_name": event.from_user.username,
            "tlg_last_name": event.from_user.last_name,
        }
        async with session.post(url, json=data) as response:
            id_resp = await response.json()
            return id_resp


async def get_user(tlg_user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://repetitor_backend/api/v1/customer/{tlg_user_id}"
        ) as response:
            val = await response.json()
            return val


async def update_user(tlg_user_id: int, data: dict):
    customer_id = await get_user(tlg_user_id)
    customer_id = customer_id[0]["id"]
    data["id"] = customer_id
    async with aiohttp.ClientSession() as session:
        url = "http://repetitor_backend/api/v1/customer"
        async with session.put(url, json=data) as response:
            id_resp = await response.json()
            return id_resp
