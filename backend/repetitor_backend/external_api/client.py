from aiohttp import web, ClientSession

app = web.Application()


async def persistent_session(app):
    app["PERSISTENT_SESSION"] = session = ClientSession()
    yield
    await session.close()


app.cleanup_ctx.append(persistent_session)
