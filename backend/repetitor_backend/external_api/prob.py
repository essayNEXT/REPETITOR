import aiohttp
# from aiohttp.web


# app.cleanup_ctx.append(persistent_session)
persistent_session = aiohttp.web.AppKey("persistent_session", aiohttp.ClientSession)

async def persistent_session(app):
   app[persistent_session] = session = aiohttp.ClientSession()
   yield
   await session.close()

async def my_request_handler(request):
   session = request.app[persistent_session]
   async with session.get("http://python.org") as resp:
       print(resp.status)