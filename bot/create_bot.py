from aiogram import Bot, Dispatcher
from utils.storages import TmpStorage
from aiogram.fsm.storage.memory import MemoryStorage


from settings import BOT_TOKEN

storage = MemoryStorage()
tmp_storage = TmpStorage()

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=storage, tmp_storage=tmp_storage)
