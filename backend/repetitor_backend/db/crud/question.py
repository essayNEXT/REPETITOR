from uuid import UUID

from asyncpg import ForeignKeyViolationError

from repetitor_backend import tables
from repetitor_backend.api.v1.question.serializers import (
    GetQuestionRequest,
    UpdateQuestionRequest,
    QuestionCreateRequest,
)


async def create(**kwargs: QuestionCreateRequest) -> UUID | str:
    """
    Create new question.
    Parameters:
        - relation: UUID of item relation, used for ForeignKey links with Item Relation, required
        - item: UUID of item, used for ForeignKey links with Item, required

    Return:
    - Question.id: UUID - primary key for new Question record - UUID type
    - str - error message in case of invalid foreign keys
    """
    check_exists = await get(**kwargs)
    if check_exists:  # якщо існує  такий запис
        return (
            f"an object with such parameters already exists id={check_exists[0].id}  "
            f"is_active={check_exists[0].is_active} "
        )
        raise TypeError(
            f"an object with such parameters already exists {check_exists[0].id}"
        )

    try:
        result = await tables.Question.insert(tables.Question(**kwargs)).returning(
            tables.Question.id
        )
    except ForeignKeyViolationError as e:
        return str(e)
    return result[0]["id"]


async def get(**get_param: GetQuestionRequest) -> list[tables.Question]:
    """
    Get a list of existing question according to match conditions:
        Parameters:
        - id: UUID of Question
        - relation: UUID of item relation, used for ForeignKey links with Item Relation
        - item: UUID of item, used for ForeignKey links with Item
        - is_active: bool
        - advanced options for filtering:
            - item__author: author of item, used for ForeignKey links with Item
            - item__context__name_short: the short name of the required items context, used for FK links with Item - str
            - item__text: the text of the required items, used for ForeignKey links with Item - str type len(2..255)

    Return:
    - List that contains the results of the query, serialized to
    the Question type
    """

    query = tables.Question.objects()
    for param, value in get_param.items():
        if value is not None:
            # Розбиваємо параметр на частини
            parts = param.split("__")

            # Перевіряємо кількість частин
            if len(parts) == 1:
                # Якщо одна частина, просто використовуємо параметр
                query = query.where(getattr(tables.Question, param, None) == value)
            elif len(parts) == 2:
                # Якщо дві частини, використовуємо вкладений виклик
                nested_attr = getattr(tables.Question, parts[0], None)
                query = query.where(getattr(nested_attr, parts[1], None) == value)
            elif len(parts) == 3:  # рекурсія нема часу зробити та протестувати
                nested_attr = getattr(tables.Question, parts[0], None)
                nested_attr = getattr(nested_attr, parts[1], None)
                query = query.where(getattr(nested_attr, parts[2], None) == value)
    result = await query
    if not result:
        return []

    return result


async def update(id: UUID, **update_param: UpdateQuestionRequest) -> UUID | None:
    """
    Update existing record in question.

    parameters:
    - id: UUID of Question, required
    - relation: UUID of item relation, used for ForeignKey links with Item Relation
    - item: UUID of item, used for ForeignKey links with Item
    - is_active: bool

    Return:
    - Question.id: UUID - primary key for question record - UUID type
    - If there is no record with this id, it returns None

    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function update question must be UUID-type, but got {type(id)}"
        )
    filtered_param = {k: v for k, v in update_param.items() if v is not None}
    result = (
        await tables.Question.update(filtered_param)
        .where(tables.Question.id == id)
        .returning(tables.Question.id)
    )
    return result[0]["id"] if result else None


async def delete(id: UUID) -> UUID | None:
    """Delete question with question.id == id.

    parameter:
    - id - UUID.
    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function del_question must be UUID-type, but got {type(id)}"
        )
    result = await update(id=id, is_active=False)
    return result
