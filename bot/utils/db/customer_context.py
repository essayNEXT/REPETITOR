import aiohttp
from uuid import UUID
from .customer import get_user


async def create_customer_context(
    customer_id: UUID, context_1_id: UUID, context_2_id: UUID
):
    async with aiohttp.ClientSession() as session:
        url = "http://repetitor_backend/api/v1/customer_context/"
        data = {
            "customer": customer_id,
            "context_1": context_1_id,
            "context_2": context_2_id,
        }
        async with session.post(url, json=data) as response:
            id_resp = await response.json()
            return id_resp


async def get_customer_context_by_user_id(user_id: int):
    user_data = await get_user(user_id)
    customer_uuid = user_data[0]["id"]
    print(customer_uuid)
    async with aiohttp.ClientSession() as session:
        url = "http://repetitor_backend/api/v1/customer_context/"
        params = {"customer": customer_uuid}
        async with session.get(url, params=params) as response:
            context = await response.json()
            return context
