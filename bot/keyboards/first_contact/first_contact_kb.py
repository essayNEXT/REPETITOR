from ..inline_keyboard import KeyboardOfDict, ContextInlineKeyboardGenerator

# from ..keyboard_translate.kb_translate import translate_context
from utils.db.customer import get_user
from utils.help import HelpConstructor


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
        # return translate_context  # на етапі розробки поки не перекладатимемо клавіатури
        return None

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


class ConfirmKeyboard(ContextInlineKeyboardGenerator, HelpConstructor):
    """Клавіатура погодження даних від користувача"""

    @property
    def initial_text(self) -> str:
        initial_text = (
            "<b>{}</b>, here what we know about you.\nDo you want to change something?"
        )
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "confirm_kb_"
        return callback_pattern

    @property
    def max_rows_number(self) -> None:
        return None

    @property
    def translate_function(self):
        # return translate_context  # на етапі розробки поки не перекладатимемо клавіатури
        return None

    @property
    def top_buttons(self) -> KeyboardOfDict:
        top_buttons = [
            [
                {
                    "callback_data": "confirm_kb_continue",
                    "text": "Continue",
                    "message": "Good! Now we need to define first user context for learning.",
                }
            ],
            [
                {
                    "callback_data": "confirm_kb_change_data",
                    "text": "Change data",
                    "message": "Change data",
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

    @staticmethod
    def help_messages() -> list[dict]:
        help_messages = [
            {
                "front_name": "Telegram",
                "state": "RegistrationForm:CONFIRM_DATA",
                "language__name_short": "en",
                "text": "Press 'Continue' if you do not want to change the data displayed in the message. Press "
                "'Change data ' if you want to change the data.",
            }
        ]
        return help_messages

    async def __user_data(self):
        user_data = await get_user(self.user_id)
        user_data = user_data[0]
        data_for_check = ["first_name", "last_name", "native_language", "email"]
        out_data = "\n".join(
            [str(key) + " : " + str(user_data[key]) for key in data_for_check]
        )
        return out_data

    async def message_text(self):
        data = await self.__user_data()
        return self.text + "\n\n" + data

    def confirm_data(self):
        return self.messages["confirm_kb_continue"]


class ChangeUserDataKeyboard(ContextInlineKeyboardGenerator, HelpConstructor):
    """Клавіатура зміни даних про користувача"""

    @property
    def initial_text(self) -> str:
        initial_text = "<b>What do you want to change?</b>\n"
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "change_"
        return callback_pattern

    @property
    def max_rows_number(self) -> None:
        return None

    @property
    def translate_function(self):
        # return translate_context  # на етапі розробки поки не перекладатимемо клавіатури
        return None

    @property
    def top_buttons(self) -> KeyboardOfDict:
        top_buttons = [
            [
                {
                    "callback_data": "change_first_name",
                    "text": "First name",
                    "message": "Enter your <b>First name</b>:",
                },
                {
                    "callback_data": "change_last_name",
                    "text": "Last name",
                    "message": "Enter your <b>Last name</b>:",
                },
            ],
            [
                {
                    "callback_data": "change_native_language",
                    "text": "Native language",
                    "message": "Enter your <b>Native language</b>:",
                },
                {
                    "callback_data": "change_email",
                    "text": "Email",
                    "message": "Enter your <b>Email</b>:",
                },
            ],
            [
                {
                    "callback_data": "change_cancel",
                    "text": "❌",
                    "message": "Cancel",
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

    @staticmethod
    def help_messages() -> list[dict]:
        help_messages = [
            {
                "front_name": "Telegram",
                "state": "RegistrationForm:CHANGE_DATA",
                "language__name_short": "en",
                "text": "Press into one of parameters 'name', 'surname', 'language' or 'email' you want to change",
            }
        ]
        return help_messages
