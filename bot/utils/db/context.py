import aiohttp


async def get_context():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://repetitor_backend/api/v1/context/") as response:
            context = await response.json()
            return context
