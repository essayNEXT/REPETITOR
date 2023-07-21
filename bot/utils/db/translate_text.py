from uuid import UUID

import aiohttp


async def get_translate_text(item_text: str, customer_tg_id: int) -> list | None:
    async with aiohttp.ClientSession() as session:
        url = "http://repetitor_backend/api/v1/translate/"
        params = {"item_text": item_text, "customer_tg_id": customer_tg_id}
        async with session.get(url, params=params) as response:
            customer_types = await response.json()
            return customer_types


async def post_user_translate(
    source_text: str,
    target_text: str,
    context_1_id_sn: list[UUID, str],
    context_2_id_sn: list[UUID, str],
    author: UUID,
):
    async with aiohttp.ClientSession() as session:
        url = "http://repetitor_backend/api/v1/creating_phrases/"
        data = {
            "source_text": source_text,
            "target_text": target_text,
            "context_1_id_sn": context_1_id_sn,
            "context_2_id_sn": context_2_id_sn,
            "author": author,
        }
        async with session.post(url, json=data) as response:
            resp = await response.json()
            return resp
