import aiohttp


async def get_translate_text(item_text: str, customer_tg_id: int) -> list | None:
    async with aiohttp.ClientSession() as session:
        url = "http://repetitor_backend/api/v1/translate/"
        params = {"item_text": item_text, "customer_tg_id": customer_tg_id}
        async with session.get(url, params=params) as response:
            customer_types = await response.json()
            return customer_types
