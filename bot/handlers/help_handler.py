from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.help.help_kb import HelpKeyboard
from aiogram.fsm.context import FSMContext
from utils.storages import TmpStorage
from create_bot import bot
from keyboards.inline_keyboard import KeyKeyboard

router = Router()


@router.callback_query(F.data == "help_remove")
async def help_remove(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == "help_thanks")
async def help_thanks(callback: CallbackQuery, tmp_storage: TmpStorage):
    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id - 1,
    )
    kb = tmp_storage[key]

    # Оновлюємо лічильний позитивних відгуків
    await kb.send_positive_feedback()

    await callback.answer(kb.positive_message())
    # await callback.message.delete()


@router.callback_query(F.data == "help_report_problem")
async def report_about_problem(callback: CallbackQuery, tmp_storage: TmpStorage):
    """Хендлер, що ловить колбек при натисканні кнопки [повідомити про проблему]."""
    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id - 1,
    )
    kb = tmp_storage[key]

    await callback.message.edit_text(
        kb.problem_report_text, reply_markup=kb.problem_report_markup()
    )


@router.callback_query(F.data == "help_problem_cancel")
async def help_problem_cancel(callback: CallbackQuery, tmp_storage: TmpStorage):
    """Хендлер, що ловить колбек при натисканні кнопки [❌] (скасувати)."""
    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id - 1,
    )
    kb = tmp_storage[key]

    await callback.message.edit_text(kb.text, reply_markup=kb.markup())


@router.callback_query(F.data.func(lambda data: data.startswith("help_problem_")))
async def help_problem_report(callback: CallbackQuery, tmp_storage: TmpStorage):
    """Хендлер, що ловить колбек при натисканні кнопки [Проблема №_] та відправляє негативний відгук."""
    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=callback.message.chat.id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id - 1,
    )
    kb = tmp_storage[key]

    # Оновлюємо лічильний негативних відгуків
    await kb.send_negative_feedback()
    # Відправляємо опис проблеми для подальшого опрацювання
    await kb.send_problem_report(callback.data)

    await callback.answer(kb.negative_message())
    # await callback.message.delete()


@router.message(Command("help"))
async def help_command(message: Message, tmp_storage: TmpStorage, state: FSMContext):
    """
    Хендлер приймає команду /help.
    З БД отримуємо та надсилаємо повідомлення допомоги для поточного стану користувача.
    """
    # Отримуємо поточний стан користувача
    user_state = await state.get_state()

    # Створюємо екземпляр клавіатури HelpKeyboard
    kb = await HelpKeyboard(
        user_language=message.from_user.language_code,
        user_id=message.from_user.id,
        user_state=user_state,
    )

    key = KeyKeyboard(
        bot_id=bot.id,
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        message_id=message.message_id,
    )
    # Записуємо екземпляр клавіатури в TmpStorage з ключем KeyKeyboard
    tmp_storage[key] = kb

    await message.answer(kb.text, reply_markup=kb.markup())
