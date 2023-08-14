from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from keyboards.text_translate.text_translate_kb import TextTranslateKeyboard
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.storages import TmpStorage
from handlers.first_contact_handler import StepsForm
from create_bot import bot
from keyboards.inline_keyboard import KeyKeyboard

router = Router()


class TranslationForm(StatesGroup):
    """Клас, що описує стани проходження перекладу."""

    ADD_USER_TRANSLATION = State()
    GET_TRANSLATION = State()


@router.callback_query(Text(text="text_translate_ok"))
async def send_translate_ok(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(None)
    await state.clear()


@router.callback_query(Text(text="text_translate_my_translation"))
async def enter_user_translation(
    callback: CallbackQuery, state: FSMContext, tmp_storage: TmpStorage
):
    """Хендлер, що ловить колбек при натисканні кнопки мій переклад."""
    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id - 1,
    )
    kb = tmp_storage[key]

    await state.update_data(last_key=key, last_message=callback.message.message_id)
    await state.set_state(TranslationForm.ADD_USER_TRANSLATION)
    await callback.message.edit_text(
        kb.message_for_user_translation(), reply_markup=kb.markup_cancel()
    )


@router.callback_query(Text(text="text_translate_cancel"))
async def enter_user_translation_cancel(
    callback: CallbackQuery, state: FSMContext, tmp_storage: TmpStorage
):
    """Хендлер, що ловить колбек при натисканні кнопки ❌ (скасувати)."""
    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id - 1,
    )
    kb = tmp_storage[key]

    await state.set_state(TranslationForm.GET_TRANSLATION)
    await callback.message.edit_text(
        kb.massage_for_translation_text(), reply_markup=kb.markup()
    )


@router.message(TranslationForm.ADD_USER_TRANSLATION)
async def add_user_translation(
    message: Message, state: FSMContext, tmp_storage: TmpStorage
):
    data = await state.get_data()
    key = data.get("last_key")
    last_message = data.get("last_message")
    kb = tmp_storage[key]
    await kb.add_user_translation(message.text)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=last_message,
        text=kb.massage_for_translation_text(),
        reply_markup=kb.markup(),
    )
    await state.clear()


@router.message()
async def translate_word(message: Message, tmp_storage: TmpStorage, state: FSMContext):
    if await state.get_state() != StepsForm.CHANGE_DATA:
        kb = await TextTranslateKeyboard(
            user_language=message.from_user.language_code,
            user_id=message.from_user.id,
            text_for_translate=message.text,
        )

        key = KeyKeyboard(
            bot_id=bot.id,
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            message_id=message.message_id,
        )
        tmp_storage[key] = kb
        await message.answer(
            kb.massage_for_translation_text(), reply_markup=kb.markup()
        )
        await state.set_state(TranslationForm.GET_TRANSLATION)
    else:
        await message.answer("⁉️")
        await message.answer("you have to choose one of the options")
