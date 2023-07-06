from aiogram import Bot, Dispatcher
from utils.storages import TmpStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession


from settings import BOT_TOKEN

storage = MemoryStorage()
tmp_storage = TmpStorage()
session = AiohttpSession()
connections = session.create_session()

bot = Bot(token=BOT_TOKEN, parse_mode="HTML", session=session)
dp = Dispatcher(storage=storage, tmp_storage=tmp_storage)
