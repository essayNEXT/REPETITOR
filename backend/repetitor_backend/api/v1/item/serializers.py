from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, Field

from repetitor_backend import tables

REGEX_PATH = r"^([a-zA-Z0-9_\\/]+)([a-zA-Z0-9_.]+)$"
"""У цьому виразі:

^ вказує на початок рядка.
([a-zA-Z0-9_\\/]+) визначає групу, яка відповідає за розподіл директорій. Вона може містити будь-яку комбінацію букв, цифр, символів підкреслення, косої риски.
([a-zA-Z0-9_.]+) визначає групу, яка відповідає за назву файлу і розширення. Вона може містити будь-яку комбінацію букв, цифр, символів підкреслення і крапки.
$ вказує на кінець рядка.
Цей вираз можна застосувати до шляху до файла і отримати відповідні групи, які будуть містити розподіл директорій і назву файлу з розширенням. Залежно від реалізації регулярних виразів, код може виглядати трохи інакше, але загальна ідея залишиться такою ж.
"""


class ItemCreateRequest(BaseModel):
    text: Annotated[str, Query(min_length=2, max_length=255)]
    image: Annotated[str | None, Query(min_length=3, max_length=255, regex=REGEX_PATH)]
    sound: Annotated[str | None, Query(min_length=3, max_length=255, regex=REGEX_PATH)]
    author: UUID | None
    context: UUID | None
    is_active: bool | None


class ItemResponse(ItemCreateRequest):
    text: Annotated[str | None, Query(min_length=2, max_length=255)]
    id: UUID


class UpdateItemRequest(ItemResponse):
    #     text: Annotated[str | None, Query(min_length=2, max_length=255)] = None
    pass


class DeleteItemRequest(ItemResponse):
    pass
