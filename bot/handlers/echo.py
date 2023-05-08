from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message()
async def echo(message:Message):
    await message.answer(message.text)
