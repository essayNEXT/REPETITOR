from typing import Union
from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from keyboards.inline_keyboard import KeyKeyboard
from keyboards.custom_inline_keyboard import MyCustomKeyboard, MyCustomKeyboard2
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.storages import TmpStorage
from create_bot import bot


class InlineStates(StatesGroup):
    Inline = State()


router = Router()


@router.message(Command(commands="test_kb"))
@router.callback_query(Text(startswith="#_test_"))
async def get_test_kb(
    event: Union[Message, CallbackQuery], state: FSMContext, tmp_storage: TmpStorage
):
    """Хендлер для тестової клавіатури MyCustomKeyboard"""
    if isinstance(event, Message):
        await state.set_state(InlineStates.Inline)

        user_language = event.from_user.language_code
        user_id = event.from_user.id
        # user_language = "uk"

        kb = MyCustomKeyboard(user_language=user_language, user_id=user_id, dp=router)

        key = KeyKeyboard(
            bot_id=bot.id,
            chat_id=event.chat.id,
            user_id=event.from_user.id if event.from_user else None,
            message_id=event.message_id,
        )
        tmp_storage[key] = kb

        await event.answer(kb.text, reply_markup=kb.markup())

    if isinstance(event, CallbackQuery):
        key = KeyKeyboard(
            bot_id=bot.id,
            chat_id=event.message.chat.id,
            user_id=event.from_user.id if event.from_user else None,
            message_id=event.message.message_id - 1,
        )
        kb = tmp_storage[key]

        kb.callback(event)

        await event.message.edit_text(kb.text, reply_markup=kb.markup())


@router.message(Command(commands="test2_kb"))
@router.callback_query(Text(startswith="#_test2_"))
async def get_test2_kb(
    event: Union[Message, CallbackQuery], state: FSMContext, tmp_storage: TmpStorage
):
    """Хендлер для тестової клавіатури MyCustomKeyboard.
    В даному прикладі ми не передаємо диспетчер в екземпляр класу і повинні відловлювати пагінацію вручну.
    Мова клавіатури відповідає мові користувача (українська) для даного прикладу."""

    if isinstance(event, Message):
        await state.set_state(InlineStates.Inline)

        # user_language = event.from_user.language_code
        user_id = event.from_user.id
        user_language = "uk"

        kb = MyCustomKeyboard2(user_language=user_language, user_id=user_id)

        key = KeyKeyboard(
            bot_id=bot.id,
            chat_id=event.chat.id,
            user_id=event.from_user.id if event.from_user else None,
            message_id=event.message_id,
        )
        tmp_storage[key] = kb

        await event.answer(kb.text, reply_markup=kb.markup())

    if isinstance(event, CallbackQuery):
        key = KeyKeyboard(
            bot_id=bot.id,
            chat_id=event.message.chat.id,
            user_id=event.from_user.id if event.from_user else None,
            message_id=event.message.message_id - 1,
        )
        kb = tmp_storage[key]
        if event.data.endswith("fast_up"):
            kb.markup_fast_up()
        elif event.data.endswith("up"):
            kb.markup_up()
        elif event.data.endswith("fast_down"):
            kb.markup_fast_down()
        elif event.data.endswith("down"):
            kb.markup_down()
        else:
            kb.callback(event)

        await event.message.edit_text(kb.text, reply_markup=kb.markup())
