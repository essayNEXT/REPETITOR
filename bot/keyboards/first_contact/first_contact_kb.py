from ..inline_keyboard import KeyboardOfDict, ContextInlineKeyboardGenerator
from ..keyboard_translate.kb_translate import translate_context
from utils.db.customer import get_user


class RegisterKeyboard(ContextInlineKeyboardGenerator):
    """Клавіатура реєстрації"""

    @property
    def initial_text(self) -> str:
        initial_text = (
            "<b>Hello, {}!\nYou need to registrate for using my functions.</b>"
        )
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "registration"
        return callback_pattern

    @property
    def max_rows_number(self) -> None:
        return None

    @property
    def translate_function(self):
        return translate_context

    @property
    def top_buttons(self) -> KeyboardOfDict:
        top_buttons = [
            [
                {
                    "callback_data": "registration",
                    "text": "Register",
                    "message": "Register",
                }
            ]
        ]
        return top_buttons

    @property
    def scroll_buttons(self) -> KeyboardOfDict | None:
        return None

    @property
    def bottom_buttons(self) -> KeyboardOfDict | None:
        return None


class ConfirmKeyboard(ContextInlineKeyboardGenerator):
    """Клавіатура погодження даних від користувача"""

    @property
    def initial_text(self) -> str:
        initial_text = "<b>Чудове рішення, {}</b>!\n\nНижче те, що ми про тебе знаємо.\nМожливо хочеш щось змінити?\n\n"
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "uk"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "confirm"
        return callback_pattern

    @property
    def max_rows_number(self) -> None:
        return None

    @property
    def translate_function(self):
        return translate_context

    @property
    def top_buttons(self) -> KeyboardOfDict:
        top_buttons = [
            [
                {
                    "callback_data": "confirm_continue",
                    "text": "Подовжити",
                    "message": "Продовжити",
                }
            ],
            [
                {
                    "callback_data": "confirm_change_data",
                    "text": "Змінити дані",
                    "message": "Змінити дані",
                }
            ],
        ]
        return top_buttons

    @property
    def scroll_buttons(self) -> KeyboardOfDict | None:
        return None

    @property
    def bottom_buttons(self) -> KeyboardOfDict | None:
        return None

    async def __user_data(self):
        user_data = await get_user(self.user_id)
        user_data = user_data[0]
        data_for_check = ["native_language", "first_name", "last_name", "email"]
        out_data = "\n".join(
            [str(key) + " : " + str(user_data[key]) for key in data_for_check]
        )
        return out_data

    async def message_text(self):
        data = await self.__user_data()
        return self.text + data
