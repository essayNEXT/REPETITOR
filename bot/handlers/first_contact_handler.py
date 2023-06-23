from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.db.customer_type import get_customer_type
from utils.db.customer import create_user


router = Router()


class StepsForm(StatesGroup):
    """Клас, що описує стани проходження реєстрації користувача."""

    INITIAL_DATA = State()
    CHANGE_DATA = State()
    CONFIRM_DATA = State()
    F_NAME_CHANGED = State()
    L_NAME_CHANGED = State()
    EMAIL_CHANGED = State()
    PHONE_CHANGED = State()


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
    new_user_uuid = await create_user(callback, customer_class)

    await callback.message.answer(
        f"Чудове рішення, {callback.from_user.first_name} твій айді {new_user_uuid}!\n"
        # "Тепер надішли мені свій контакт або можеш все скасувати.\n",
        # reply_markup=get_contact_kb()
    )
    await state.set_state(StepsForm.INITIAL_DATA)
