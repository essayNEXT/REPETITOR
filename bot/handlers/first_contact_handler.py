from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.db.customer_type import get_customer_type
from utils.db.customer import create_user, update_user
from utils.storages import TmpStorage
from pydantic import BaseModel, EmailStr, ValidationError

from keyboards.first_contact.first_contact_kb import (
    ConfirmKeyboard,
    ChangeUserDataKeyboard,
)
from keyboards.user_context.user_context_kb import ChooseContextKeyboard
from keyboards.native_language.native_language_kb import ChooseNativeLanguageKeyboard

from keyboards.inline_keyboard import KeyKeyboard
from create_bot import bot
from .customer_context_handler import CreateContextStepsForm
import json

router = Router()


class Email(BaseModel):
    email: EmailStr


class StepsForm(StatesGroup):
    """Клас, що описує стани проходження реєстрації користувача."""

    CONFIRM_DATA = State()
    CHANGE_DATA = State()
    F_NAME_CHANGED = State()
    L_NAME_CHANGED = State()
    NATIVE_LANGUAGE_SELECTING = State()
    EMAIL_CHANGED = State()


@router.callback_query(Text(text="registration"))
async def registration(
    callback: CallbackQuery, state: FSMContext, tmp_storage: TmpStorage
):
    """Хендлер, що ловить колбек при натисканні кнопки 'Зареєструватись' від користувача."""
    # Видаляємо кнопку реєстрації, щоб користувач не міг натискати її безліч разів
    await callback.message.delete()

    # Заносимо користувача в БД
    customer_type = await get_customer_type("user")
    customer_type = customer_type["id"]
    new_user_uuid = await create_user(callback, customer_type)
    print("New customer id: ", new_user_uuid)

    if new_user_uuid:
        kb = await ConfirmKeyboard(
            user_language=callback.from_user.language_code,
            user_id=callback.from_user.id,
        )

        text = await kb.message_text()

        await callback.message.answer(
            text.format(callback.from_user.first_name), reply_markup=kb.markup()
        )
        await state.set_state(StepsForm.CONFIRM_DATA)
    else:
        await callback.message.delete(
            chat_id=callback.message.chat.id, message_id=callback.message.message_id
        )


@router.callback_query(StepsForm.CONFIRM_DATA, Text(text="confirm_kb_continue"))
async def confirm_data(
    callback: CallbackQuery, state: FSMContext, tmp_storage: TmpStorage
):
    """Обробка кнопки підтвердження персональних даних"""
    kb = await ChooseContextKeyboard(
        user_language=callback.from_user.language_code,
        user_id=callback.from_user.id,
        dp=router,
    )

    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id - 1,
    )
    tmp_storage[key] = kb

    await callback.message.edit_text(kb.text, reply_markup=kb.markup())
    await state.set_state(CreateContextStepsForm.CREATE_CUSTOMER_CONTEXT)


@router.callback_query(
    StepsForm.NATIVE_LANGUAGE_SELECTING, Text(text="native_language_back")
)
@router.callback_query(StepsForm.CONFIRM_DATA, Text(text="confirm_kb_change_data"))
async def change_data(
    callback: CallbackQuery, state: FSMContext, tmp_storage: TmpStorage
):
    """Обробка кнопки зміни персональних даних"""

    kb = await ChangeUserDataKeyboard(
        user_language=callback.from_user.language_code, user_id=callback.from_user.id
    )

    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id - 1,
    )
    tmp_storage[key] = kb

    await callback.message.edit_text(kb.text, reply_markup=kb.markup())
    await state.set_state(StepsForm.CHANGE_DATA)


@router.callback_query(StepsForm.CHANGE_DATA, Text(startswith="change_"))
async def choose_data_to_change(
    callback: CallbackQuery, state: FSMContext, tmp_storage: TmpStorage
):
    """Хендлер, що ловить колбек при натисканні кнопки зміни визначеного параметра від користувача.
    Виводить повідомляння з проханням вказати необхідний параметр та змінює стан згідно з параметром, що змінено.
    """
    if callback.data == "change_native_language":
        kb = await ChooseNativeLanguageKeyboard(
            user_language=callback.from_user.language_code,
            user_id=callback.from_user.id,
            dp=router,
        )

        key = KeyKeyboard(
            bot_id=bot.id,
            chat_id=callback.message.chat.id,
            user_id=callback.from_user.id,
            message_id=callback.message.message_id,
        )
        tmp_storage[key] = kb
        await callback.message.edit_text(kb.text, reply_markup=kb.markup())
        await state.set_state(StepsForm.NATIVE_LANGUAGE_SELECTING)
    else:
        key = KeyKeyboard(
            bot_id=bot.id,
            chat_id=callback.message.chat.id,
            user_id=callback.from_user.id,
            message_id=callback.message.message_id - 1,
        )
        kb = tmp_storage[key]

        await callback.message.delete()
        await callback.answer()

    # перевіряємо вхідний колбек згідно з параметрами, які необхідно змінити
    if callback.data == "change_first_name":
        await callback.message.answer(kb.messages["change_first_name"])
        await state.set_state(StepsForm.F_NAME_CHANGED)
    elif callback.data == "change_last_name":
        await callback.message.answer(kb.messages["change_last_name"])
        await state.set_state(StepsForm.L_NAME_CHANGED)
    elif callback.data == "change_email":
        await callback.message.answer(kb.messages["change_email"])
        await state.set_state(StepsForm.EMAIL_CHANGED)


@router.callback_query(
    StepsForm.NATIVE_LANGUAGE_SELECTING, Text(startswith="native_language_")
)
async def selecting_native_language(
    callback: CallbackQuery, state: FSMContext, tmp_storage: TmpStorage
):
    """Хендлер, що ловить колбек при натисканні кнопок у меню вибору рідної мови користувача."""
    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id,
    )
    kb = tmp_storage[key]

    if callback.data == "native_language_done":
        if kb.validation[0]:
            await kb.update_user_native_language()

            kb = await ConfirmKeyboard(
                user_language=callback.from_user.language_code,
                user_id=callback.from_user.id,
            )

            text = await kb.message_text()
            await callback.message.edit_text(
                text.format(callback.from_user.first_name), reply_markup=kb.markup()
            )
            await state.set_state(StepsForm.CONFIRM_DATA)
        else:
            await callback.answer()
    else:
        kb.validation[0] = True
        kb.selected_data[0] = callback.data
        await callback.message.edit_text(
            kb.language_selection_text(), reply_markup=kb.markup()
        )


@router.message(StepsForm.F_NAME_CHANGED)
@router.message(StepsForm.L_NAME_CHANGED)
@router.message(StepsForm.EMAIL_CHANGED)
async def update_user_data(message: Message, state: FSMContext):
    """Хендлер, що обробляє зміну даних отриманих від користувача.
    Виводить колбек-кнопки 'змінити' та 'продовжити'."""
    user_state = await state.get_state()

    key = None
    if user_state == StepsForm.F_NAME_CHANGED:
        key = "first_name"
    elif user_state == StepsForm.L_NAME_CHANGED:
        key = "last_name"
    elif user_state == StepsForm.EMAIL_CHANGED:
        key = "email"

    data = {key: message.text}

    if key == "email":
        email_data = json.dumps(data)
        try:
            Email.parse_raw(email_data)
            await update_user(message.from_user.id, data)
            await message.answer("✅")
        except ValidationError:
            await message.answer("Invalid email")
            await message.answer("❌")
    else:
        await update_user(message.from_user.id, data)
        await message.answer("✅")

    kb = await ConfirmKeyboard(
        user_language=message.from_user.language_code, user_id=message.from_user.id
    )

    text = await kb.message_text()
    await message.answer(
        text.format(message.from_user.first_name), reply_markup=kb.markup()
    )
    await state.set_state(StepsForm.CONFIRM_DATA)
