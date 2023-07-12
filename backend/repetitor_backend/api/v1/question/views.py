import logging

from typing import List, Annotated
from uuid import UUID
from fastapi import APIRouter, Query

from repetitor_backend import tables
from .serializers import (
    QuestionCreateRequest,
    UpdateQuestionRequest,
    GetQuestionRequest,
    GetQuestionResponse,
)
from repetitor_backend.db.crud import question

logger = logging.getLogger()

router = APIRouter()


@router.post("/question/")
async def create_question(
    new_question: QuestionCreateRequest,
) -> UUID | str:
    """
    Create new question.
    Parameters:
    - relation: UUID of item relation, used for ForeignKey links with Item Relation, required
    - item: UUID of item, used for ForeignKey links with Item, required

    Return:
    - Question.id: UUID - primary key for new question record - UUID type
    - str - error message in case of invalid foreign keys
    """
    return await question.create(**new_question.dict())


@router.get(
    "/question/",
    response_model=List[GetQuestionResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_question(
    id: UUID | None = None,
    relation: UUID = None,
    item: UUID = None,
    is_active: bool = True,
    item__author: UUID = None,
    item__context__name_short: Annotated[
        str | None, Query(min_length=2, max_length=10)
    ] = None,
    item__text: Annotated[str | None, Query(min_length=2, max_length=255)] = None,
) -> list:
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
    get_param_question = GetQuestionRequest(
        id=id,
        relation=relation,
        item=item,
        is_active=is_active,
        item__author=item__author,
        item__context__name_short=item__context__name_short,
        item__text=item__text,
    )
    results = await question.get(**get_param_question.dict())
    fin_result = [
        result.to_dict() for result in results if isinstance(result, tables.Question)
    ]
    return fin_result


@router.patch("/question/")
async def update_question(
    id: UUID, update_param_question: UpdateQuestionRequest
) -> UUID | None:
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

    return await question.update(id=id, **update_param_question.dict())


@router.delete("/question/")
async def delete_question(id_param: UUID) -> UUID | None:
    """
    Delete question with question.id == id.

    Parameter:
    - id - UUID.

    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """

    return await question.delete(id_param)
