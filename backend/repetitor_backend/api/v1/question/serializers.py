from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel


class QuestionCreateRequest(BaseModel):
    relation: UUID
    item: UUID


class UpdateQuestionRequest(BaseModel):
    relation: UUID
    item: UUID
    is_active: bool = True


class GetQuestionRequest(UpdateQuestionRequest):
    id: UUID | None
    relation: UUID | None
    item: UUID | None
    is_active: bool | None
    item__author: UUID | None
    item__context__name_short: Annotated[str | None, Query(min_length=2, max_length=10)]
    item__text: Annotated[str | None, Query(min_length=2, max_length=255)]


class GetQuestionResponse(BaseModel):
    id: UUID
    relation: UUID
    item: UUID
    is_active: bool
