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
    Create new customer context.

    Parameters:
    - customer: UUID of customer, used for ForeignKey links with Customer, required
    - context_1: UUID of context, used for ForeignKey links with Context, required
    - context_2: UUID of context, used for ForeignKey links with Context, required

    Return:
    - Question.id: UUID - primary key for new customer context record - UUID type
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
) -> list:
    """
    Get a list of existing customer context according to match conditions:

    Parameters:
    - id: UUID of customer context
    - customer: UUID of customer, used for ForeignKey links with Customer
    - context_1: UUID of context, used for ForeignKey links with Context
    - context_2: UUID of context, used for ForeignKey links with Context
    - last_date: customer context creation/update time, UTС zone
    - is_active: bool = True

    Return:
    - List that contains the results of the query
    """
    get_param_question = GetQuestionRequest(
        id=id,
        relation=relation,
        item=item,
        is_active=is_active,
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
    Update existing record in customer context.

    Parameters:
    - id: UUID of customer context, required
    - customer: UUID of customer, used for ForeignKey links with Customer
    - context_1: UUID of context, used for ForeignKey links with Context
    - context_2: UUID of context, used for ForeignKey links with Context
    - last_date: customer context creation/update time, UTС zone
    - is_active: bool = True

    Return:
    - Question.id: UUID - primary key for new customer context record - UUID type
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
