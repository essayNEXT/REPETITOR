from microsoft_v2 import translate
import asyncio
import aiohttp

# async def gather_data():
#
#
#     async with aiohttp.ClientSession() as session:
#         response = await session.get(url=url, headers=headers)
#
#
#         tasks = []
#
#         for page in range(1, pages_count + 1):
#             task = asyncio.create_task(get_page_data(session, page))
#             tasks.append(task)
#
#         await asyncio.gather(*tasks)

async def test_microsoft():
    async with aiohttp.ClientSession() as session:
      result = await translate(session, "uk", "en", "я йду гуляти", )
    print(result)


if __name__ == "__main__":
    asyncio.run(test_microsoft())
