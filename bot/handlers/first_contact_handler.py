from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.db.customer_type import get_customer_type
from utils.db.customer import create_user
from keyboards.first_contact.first_contact_kb import ConfirmKeyboard

router = Router()


class StepsForm(StatesGroup):
    """Клас, що описує стани проходження реєстрації користувача."""

    CONFIRM_DATA = State()


@router.callback_query(Text(text="registration"))
async def cmd_start(callback: CallbackQuery, state: FSMContext):
    """Хендлер, що ловить колбек при натисканні кнопки 'Зареєструватись' від користувача."""
    # Видаляємо кнопку реєстрації, щоб користувач не міг натискати її безліч разів
    await callback.message.delete()

    # Заносимо користувача в БД
    customer_class = await get_customer_type(
        "student"
    )  # Після визначення основних ролей змінимо на стандартний тип
    customer_class = customer_class["id"]
    await create_user(callback, customer_class)

    kb = ConfirmKeyboard(
        user_language=callback.from_user.language_code, user_id=callback.from_user.id
    )
    text = await kb.message_text()

    await callback.message.answer(
        text.format(callback.from_user.first_name),
        reply_markup=kb.markup(),
    )
    await state.set_state(StepsForm.CONFIRM_DATA)


@router.callback_query(StepsForm.CONFIRM_DATA)
async def confirm_data(callback: CallbackQuery, state: FSMContext):
    """Обробка кнопок підтвердження або зміни персональних даних"""
    await callback.message.edit_text("Дякую! Попрацюємо!")
    await state.clear()
