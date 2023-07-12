from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, validator


class GetItemRelationViewRequest(BaseModel):
    item_text: Annotated[str, Query(min_length=2, max_length=255)]
    item_author: UUID
    item_context_name_short_1: Annotated[str, Query(min_length=2, max_length=10)]
    item_context_name_short_2: Annotated[str, Query(min_length=2, max_length=10)]
    is_active: bool | None

    @validator("item_context_name_short_2")
    def validate_context_2(cls, value, values):
        if "context_1" in values and value == values["item_context_name_short_1"]:
            raise ValueError("context_2 must have a different value than context_1")
        return value


item_relation: UUID


class GetItemRelationViewResponse(BaseModel):
    item_relation: UUID
    item_text_1: Annotated[str, Query(min_length=2, max_length=255)]
    item_author_1: UUID
    item_context_name_short_1: Annotated[str, Query(min_length=2, max_length=10)]
    question: UUID
    right_answ_item: UUID
    item_text_2: Annotated[str, Query(min_length=2, max_length=255)]
    item_author_2: UUID
    item_context_name_short_2: Annotated[str, Query(min_length=2, max_length=10)]
    is_active: bool


class UpdateItemRelationViewRequest(BaseModel):
    pass
