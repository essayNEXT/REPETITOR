from aiogram import Router
from aiogram.filters import Text, Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.storages import TmpStorage
from keyboards.user_context.user_context_kb import ChooseContextKeyboard
from keyboards.inline_keyboard import KeyKeyboard
from create_bot import bot
from utils.db.customer_context import get_customer_context_by_user_id

router = Router()


class CreateContextStepsForm(StatesGroup):
    """Клас, що описує стани проходження реєстрації користувача."""

    CREATE_CUSTOMER_CONTEXT = State()
    CHOOSE_FIRST_CONTEXT = State()
    FIRST_CONTEXT_CHOSEN = State()
    CHOOSE_SECOND_CONTEXT = State()
    SECOND_CONTEXT_CHOSEN = State()


@router.callback_query(Text(text="settings_add_customer_context"))
async def create_customer_context(
    callback: CallbackQuery, state: FSMContext, tmp_storage: TmpStorage
):
    """Обробка натискання кнопки створити новий контекст користувача"""
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
    CreateContextStepsForm.CREATE_CUSTOMER_CONTEXT,
    Text(startswith="create_user_context_con_"),
)
async def choose_context(
    callback: CallbackQuery, state: FSMContext, tmp_storage: TmpStorage
):
    """Обробка кнопки Базового чи Цільового вибору контексту мови для створення контексту користувача"""

    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id - 1,
    )
    kb = tmp_storage[key]

    if callback.data == "create_user_context_con_1":
        kb.selected_data[0] = callback.data
        kb.validation[0] = False
        await state.set_state(CreateContextStepsForm.CHOOSE_FIRST_CONTEXT)
    elif callback.data == "create_user_context_con_2":
        kb.selected_data[1] = callback.data
        kb.validation[1] = False
        await state.set_state(CreateContextStepsForm.CHOOSE_SECOND_CONTEXT)

    await callback.message.edit_text(
        kb.context_selection_text(), reply_markup=kb.markup()
    )


@router.callback_query(
    CreateContextStepsForm.CHOOSE_FIRST_CONTEXT,
    Text(startswith="create_user_context_lng_"),
)
@router.callback_query(
    CreateContextStepsForm.CHOOSE_SECOND_CONTEXT,
    Text(startswith="create_user_context_lng_"),
)
async def choose_context_lng(
    callback: CallbackQuery, state: FSMContext, tmp_storage: TmpStorage
):
    """Обробка кнопки вибору контексту мови для створення контексту користувача серед переліку"""

    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id - 1,
    )
    kb = tmp_storage[key]

    current_state = await state.get_state()
    if current_state == CreateContextStepsForm.CHOOSE_FIRST_CONTEXT:
        kb.selected_data[0] = callback.data
        kb.validation[0] = True
        await state.set_state(CreateContextStepsForm.CREATE_CUSTOMER_CONTEXT)
    elif current_state == CreateContextStepsForm.CHOOSE_SECOND_CONTEXT:
        kb.selected_data[1] = callback.data
        kb.validation[1] = True
        await state.set_state(CreateContextStepsForm.CREATE_CUSTOMER_CONTEXT)
    await callback.message.edit_text(
        kb.context_selection_text(), reply_markup=kb.markup()
    )


@router.callback_query(
    CreateContextStepsForm.CREATE_CUSTOMER_CONTEXT,
    Text(text="create_user_context_done"),
)
async def approve_customer_context(
    callback: CallbackQuery, state: FSMContext, tmp_storage: TmpStorage
):
    """Обробка кнопки погодити створення контексту користувача"""

    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id - 1,
    )
    kb = tmp_storage[key]

    if kb.validation[0] and kb.validation[1]:
        if kb.selected_data[0] != kb.selected_data[1]:
            await kb.create_customer_context()
            await callback.message.edit_text(kb.messages[callback.data])
            await state.clear()


@router.message(Command(commands="my_contexts"))
async def my_user_contexts(message: Message):
    result = await get_customer_context_by_user_id(message.from_user.id)
    await message.answer(str(result))
