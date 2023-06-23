from aiogram import Dispatcher, Router
from itertools import chain, islice
from typing import List, Dict, Callable
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from dataclasses import dataclass
from aiogram.types import CallbackQuery
from aiogram.filters import Text

# from enum import Enum
from abc import ABC, abstractmethod

# Оголошення типів для створення клавіатури
ButtonDict = Dict[str, str]  # Словник з даними для формування InlineKeyboardButton
RawOfButtonDict = List[
    ButtonDict
]  # Список зі словниками для формування InlineKeyboardButton, що утворює ряд
KeyboardOfDict = List[
    RawOfButtonDict
]  # Цілісний список з рядами кнопок у вигляді словника
RawOfInlineButton = List[InlineKeyboardButton]  # Список об'єктів InlineKeyboardButton
KeyboardOfInlineButton = List[
    RawOfInlineButton
]  # Цілісний список з рядами кнопок у форматі InlineKeyboardButton
PagesForScroll = List[
    List[List[InlineKeyboardButton]]
]  # Список з KeyboardOfInlineButton, які утворюють сторінки


@dataclass(frozen=True)
class KeyKeyboard:
    """Описує ключ для ідентифікації примірника клавіатури та повідомлення."""

    __slots__ = ["bot_id", "chat_id", "user_id", "message_id"]

    bot_id: int
    chat_id: int
    user_id: int | None
    message_id: int


class ScrollInlineKeyboardGenerator:
    """
    Створює скролінг об'єкт клавіатури. Пагінація клавіатури виконується вертикально.
    Приймає параметри при ініціації екземпляра класу:
        - scroll_keys: KeyboardOfInlineButton - список списків кнопок прокручування
        - dp: Dispatcher | Router | None = None - диспетчер або роутер для уловлювання колбеків
    Наступні параметри визначаються в класі нащадку:
        - max_rows_number: int - максимальна кількість об'єктів прокручування
        - callback_pattern: str - шаблон колбеку класу клавіатури нащадка
    Наступні параметри створюються під час виконання пагінації клавіатури:
        - pages: PagesForScroll - змінна, що містить об'єкти KeyboardOfInlineButton, які утворюють сторінками пагінації
        - start_page: int - початкова сторінка пагінації
    """

    pages: PagesForScroll
    start_page: int
    callback_pattern: str
    max_rows_number: int

    def __init__(
        self, scroll_keys: KeyboardOfInlineButton, dp: Dispatcher | Router | None = None
    ) -> None:
        self.scroll_keys = scroll_keys

        # створюємо сторінки для пагінації
        self.create_pages()

        # Далі створюємо кнопки пагінації.
        # Для коректного відловлювання колбеку пагінації та уникнення ситуацій, коли натискання на пагінацію
        # в одному повідомленні, змінює всі повідомлення з тим самим класом клавіатури значення для
        # callback_data створюємо за шаблоном "{prefix}scroll_...",
        # якщо передано dp то prefix = id(self), якщо ні, то prefix = self.callback_pattern
        if len(self.pages) > 1:
            # перевіряємо чи було передано до екземпляра класу хендлер або роутер, якщо так, то реєструємо хендлер
            if dp:
                prefix = id(self)
                print(
                    "PAGINATION: Register pagination handler for callback_query in dp!"
                )
                self.dp = dp
                self.dp.callback_query.register(
                    self._scroll_kb, Text(startswith=f"{prefix}scroll_")
                )
            else:
                prefix = self.callback_pattern

            self.up_key = InlineKeyboardButton(
                text="⬆️", callback_data=f"{prefix}scroll_up"
            )
            self.fast_up_key = InlineKeyboardButton(
                text="⏫️", callback_data=f"{prefix}scroll_fast_up"
            )
            self.down_key = InlineKeyboardButton(
                text="⬇️", callback_data=f"{prefix}scroll_down"
            )
            self.fast_down_key = InlineKeyboardButton(
                text="⏬️", callback_data=f"{prefix}scroll_fast_down"
            )
        else:
            print(
                "PAGINATION: All scroll buttons in one page, check value of max_rows_number!"
            )

    async def _scroll_kb(self, call: CallbackQuery):
        """Хендлер обробки колбеків від кнопок вверх та вниз"""
        if call.data.endswith("fast_up"):
            self.markup_fast_up()
        elif call.data.endswith("up"):
            self.markup_up()
        elif call.data.endswith("fast_down"):
            self.markup_fast_down()
        elif call.data.endswith("down"):
            self.markup_down()
        await call.message.edit_reply_markup(reply_markup=self.markup())

    def create_pages(self) -> None:
        """Створює сторінки пагінації клавіатури скролінгу залежно від змінної max_rows_number"""
        self.pages = []
        self.start_page = 0

        iterable_scroll_keys = iter(self.scroll_keys)

        pages_iterator = iter(
            lambda: list(islice(iterable_scroll_keys, self.max_rows_number)), []
        )
        for page in pages_iterator:
            self.pages.append(page)

    def _get_current_scroll_keyboard_list(self) -> KeyboardOfInlineButton:
        """
        Повертає поточний список скролінгової клавіатури.
        Формує рядок кнопок пагінації залежно від поточної сторінки self.start_page.
        Рядок пагінації розміщується перед кнопками скролінг клавіатури.
        """
        page_index_button = InlineKeyboardButton(
            text=f"{self.start_page + 1}/{len(self.pages)}", callback_data="pass"
        )
        if not self.pages:
            return []
        elif len(self.pages) == 1:
            return self.pages[0]
        elif self.start_page == len(self.pages) - 1:
            paginator_raw = [[self.fast_up_key, self.up_key, page_index_button]]
            return paginator_raw + self.pages[self.start_page]
        elif self.start_page == 0:
            paginator_raw = [[page_index_button, self.down_key, self.fast_down_key]]
            return paginator_raw + self.pages[self.start_page]
        else:
            paginator_raw = [
                [
                    self.fast_up_key,
                    self.up_key,
                    page_index_button,
                    self.down_key,
                    self.fast_down_key,
                ]
            ]
            return paginator_raw + self.pages[self.start_page]

    def markup(self) -> InlineKeyboardMarkup:
        """Повертає теперішній стан скролінг клавіатури."""
        return InlineKeyboardMarkup(
            inline_keyboard=self._get_current_scroll_keyboard_list()
        )

    def markup_up(self) -> InlineKeyboardMarkup:
        """
        Повертає клавіатуру на 'одну сторінку вверх'.
        Змінює значення внутрішніх змінних, які зберігаються в стані клавіатури після кроку 'вверх'
        і повертає новий об'єкт клавіатури.
        """
        self.start_page -= 1
        return self.markup()

    def markup_down(self) -> InlineKeyboardMarkup:
        """
        Повертає клавіатуру на 'одну сторінку вниз'.
        Змінює значення внутрішніх змінних, які зберігаються в стані клавіатури після кроку 'вниз'
        і повертає новий об'єкт клавіатури.
        """
        self.start_page += 1
        return self.markup()

    def markup_fast_up(self) -> InlineKeyboardMarkup:
        """
        Повертає клавіатуру на першу сторінку пагінації.
        Змінює значення внутрішніх змінних, які зберігаються в стані клавіатури після кроку 'швидко_вверх'
        і повертає новий об'єкт клавіатури.
        """
        self.start_page = 0
        return self.markup()

    def markup_fast_down(self) -> InlineKeyboardMarkup:
        """
        Повертає клавіатуру на останню сторінку пагінації.
        Змінює значення внутрішніх змінних, які зберігаються в стані клавіатури після кроку 'швидко_вниз'
        і повертає новий об'єкт клавіатури.
        """
        self.start_page = len(self.pages) - 1
        return self.markup()


class CombineInlineKeyboardGenerator(ScrollInlineKeyboardGenerator):
    """
    Створює комбінований об'єкт клавіатури: скролінг та додаткові верхні та нижні кнопки.
    Приймає наступні параметри:
        - scroll_keys: KeyboardOfInlineButton список скролінг кнопок клавіатури InlineKeyboardButton
        - top_static_keys: KeyboardOfInlineButton список верхніх кнопок клавіатури InlineKeyboardButton
        - bottom_static_keys: KeyboardOfInlineButton список верхніх кнопок клавіатури InlineKeyboardButton
        - dp: Dispatcher | Router | None = None - диспетчер або роутер для уловлювання колбеків
    """

    def __init__(
        self,
        scroll_keys: KeyboardOfInlineButton,
        top_static_keys: KeyboardOfInlineButton,
        bottom_static_keys: KeyboardOfInlineButton,
        dp: Dispatcher | Router | None = None,
    ) -> None:
        super().__init__(scroll_keys, dp)

        self.top_static_keys = top_static_keys
        self.bottom_static_keys = bottom_static_keys

    def markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=list(
                chain(
                    self.top_static_keys,
                    self._get_current_scroll_keyboard_list(),
                    self.bottom_static_keys,
                )
            )
        )


class ContextInlineKeyboardGenerator(CombineInlineKeyboardGenerator, ABC):
    """
    Клас-шаблон для створення клавіатури.
    Параметри класу:
        - user_language: str - мова користувача, цільова мова перекладу
        - user_id: int - id номер користувача telegram
        - kb_language: str - мова на якій створено клас клавіатури
        - callback_pattern: str - шаблон колбеку класу клавіатури
        - initial_text: str - початковий текст при виклику клавіатури
        - top_buttons: List[List[Dict[str, str]]] | KeyboardOfDict  - список словників верхніх кнопок
        - scroll_buttons: List[List[Dict[str, str]]] | KeyboardOfDict - список словників скролінг кнопок
        - bottom_buttons: List[List[Dict[str, str]]] | KeyboardOfDict - список словників нижніх кнопок
        - max_rows_number: int - максимальна кількість об'єктів на на сторінці пагінації скролінг клавіатури
        - dp: Dispatcher | Router | None = None - диспетчер або роутер для уловлювання колбеків
    """

    def __init__(
        self,
        user_language: str,
        user_id: int = None,
        dp: Dispatcher | Router | None = None,
    ) -> None:
        # Мова користувача, використовується як цільова мова перекладу
        self.user_language = user_language

        # Використовуємо за необхідності адаптувати інформацію відносно користувача
        self.user_id = user_id

        # змінна, що накопичує в собі повідомлення кнопок, які доступні за ключем callback_data відповідної кнопки
        self.messages = {}

        # Словник з даними, які мають бути перекладені на мову користувача
        data_for_translate = {
            "initial_text": self.initial_text,
            "top_buttons": self.top_buttons,
            "scroll_buttons": self.scroll_buttons,
            "bottom_buttons": self.bottom_buttons,
        }

        # якщо не визначена функція перекладу, то data_for_translate не перекладається
        if self.translate_function is None:
            print(
                "TRANSLATOR: translate_function is None, multilanguage keyboard is not supported!"
            )
            self.translated_data = data_for_translate
        else:
            self.translated_data = self.translate_function(
                self_object=self, context_data=data_for_translate
            )

        self.text = self.translated_data["initial_text"]

        scroll_keys = self._create_buttons_list(self.translated_data["scroll_buttons"])
        top_static_keys = self._create_buttons_list(self.translated_data["top_buttons"])
        bottom_static_keys = self._create_buttons_list(
            self.translated_data["bottom_buttons"]
        )

        super().__init__(scroll_keys, top_static_keys, bottom_static_keys, dp)

    def _create_buttons_list(self, dict_list: KeyboardOfDict) -> KeyboardOfInlineButton:
        """
        Функція приймає dict_list:List[List[Dict[str, str]]] та повертає об'єкт списку списків з інлайн клавіатурами
        типу List[List[InlineKeyboardButton]], що необхідно для подальшого формування клавіатури.
        При створенні клавіатури заповнюється словник даних self.messages, що відповідає за повідомлення при натисканні
        кнопок.
        """
        if dict_list is None:
            return []
        buttons_list = []
        for item in dict_list:
            if isinstance(item, list):
                buttons_list.append(self._create_buttons_list(item))
            elif isinstance(item, dict):
                callback_data = item["callback_data"]
                text = item["text"]
                if "message" in item.keys():
                    message = item["message"]
                    self.messages[callback_data] = message
                buttons_list.append(
                    InlineKeyboardButton(text=text, callback_data=callback_data)
                )
        return buttons_list

    @property
    def text(self) -> str:
        """Повертає self._text"""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        """Змінює або задає self._text"""
        self._text = value

    @property
    @abstractmethod
    def initial_text(self) -> str:
        """Абстрактний метод для визначення початкового тексту клавіатури."""
        pass

    @property
    @abstractmethod
    def kb_language(self) -> str:
        """Абстрактний метод для визначення мови клавіатури."""
        pass

    @property
    @abstractmethod
    def callback_pattern(self) -> str:
        """Абстрактний метод для визначення шаблону колбеку."""
        pass

    @property
    @abstractmethod
    def max_rows_number(self) -> int:
        """Абстрактний метод для визначення максимальної кількості рядків скролінг клавіатури."""
        pass

    @property
    @abstractmethod
    def translate_function(self) -> Callable:
        """Абстрактний метод для визначення функції перекладу."""
        pass

    @property
    @abstractmethod
    def top_buttons(self) -> KeyboardOfDict | None:
        """Абстрактний метод для визначення верхніх кнопок клавіатури."""
        pass

    @property
    @abstractmethod
    def scroll_buttons(self) -> KeyboardOfDict | None:
        """Абстрактний метод для визначення скролінг кнопок клавіатури."""
        pass

    @property
    @abstractmethod
    def bottom_buttons(self) -> KeyboardOfDict | None:
        """Абстрактний метод для визначення нижніх кнопок клавіатури."""
        pass
