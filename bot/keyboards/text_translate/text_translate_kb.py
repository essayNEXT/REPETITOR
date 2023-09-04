from aiogram import Dispatcher, Router

from ..inline_keyboard import KeyboardOfDict, ContextInlineKeyboardGenerator

# from ..keyboard_translate.kb_translate import translate_context
from asyncinit import asyncinit
from utils.db.translate_text import get_translate_text, post_user_translate

from utils.db.customer import get_user
from utils.help import HelpConstructor


@asyncinit
class TextTranslateKeyboard(ContextInlineKeyboardGenerator, HelpConstructor):
    """Клавіатура перекладу слів"""

    async def __init__(
        self,
        user_language: str,
        text_for_translate: str,
        user_id: int = None,
        dp: Dispatcher | Router | None = None,
    ):
        self.text_for_translate = text_for_translate
        self.data_from_backend = await get_translate_text(text_for_translate, user_id)

        await super().__init__(user_language, user_id, dp)

    @property
    def initial_text(self) -> str:
        initial_text = '<b>This is translate of your word "{}" - "{}" </b>'
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "text_translate_"
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
                    "callback_data": "text_translate_ok",
                    "text": "Ok",
                    "message": "Ok",
                },
                {
                    "callback_data": "text_translate_my_translation",
                    "text": "My translation",
                    "message": 'Enter your translation for word "{}" :',
                },
            ]
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
                "state": "TranslationForm:ADD_USER_TRANSLATION",
                "language__name_short": "en",
                "text": "Enter your translation to word please",
            },
            {
                "front_name": "Telegram",
                "state": "TranslationForm:GET_TRANSLATION",
                "language__name_short": "en",
                "text": "Add word to learn or add our translation",
            },
        ]
        return help_messages

    def massage_for_translation_text(self):
        translated_text = self.data_from_backend[0]["item_text_2"]
        result = self.text.format(self.text_for_translate, translated_text)
        return result

    def message_for_user_translation(self):
        return self.messages["text_translate_my_translation"].format(
            self.text_for_translate
        )

    async def add_user_translation(self, user_translation):
        source_text = self.text_for_translate
        target_text = user_translation
        context_1_id_sn = self.data_from_backend[0]["context_1_id_sn"]
        context_2_id_sn = self.data_from_backend[0]["context_2_id_sn"]
        author = await get_user(self.user_id)
        author = author[0]["id"]
        result = await post_user_translate(
            source_text, target_text, context_1_id_sn, context_2_id_sn, author
        )
        self.data_from_backend = result
        # return result
