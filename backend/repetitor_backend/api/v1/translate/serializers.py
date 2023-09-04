from typing import Annotated
from uuid import UUID

from fastapi import Query, HTTPException
from pydantic import BaseModel, validator

from repetitor_backend.db.crud.item_relation_view import (
    REPETITOR_EXPLANATION_UUID,
    MICROSOFT_UUID,
    REPETITOR_TYPE_UUID,
)


class CreatingPhrasesRequest(BaseModel):
    source_text: Annotated[str, Query(min_length=2, max_length=255)]
    target_text: Annotated[str, Query(min_length=2, max_length=255)]
    context_1_id_sn: tuple[UUID, Annotated[str, Query(min_length=2, max_length=10)]]
    context_2_id_sn: tuple[UUID, Annotated[str, Query(min_length=2, max_length=10)]]
    author: UUID = MICROSOFT_UUID
    explanation: UUID = REPETITOR_EXPLANATION_UUID
    type: UUID = REPETITOR_TYPE_UUID
    is_active: bool = True

    @validator("context_2_id_sn")
    def validate_context_2(cls, value, values):
        if "context_1" in values and value == values["context_1_id_sn"]:
            raise HTTPException(
                status_code=404,
                detail="context_2_id_sn must have a different value than context_1_id_sn",
            )
        return value


class GetItemRelationViewResponse(BaseModel):
    item_relation: UUID
    item_text_1: Annotated[str, Query(min_length=2, max_length=255)]
    item_author_1: UUID
    context_1_id_sn: tuple[UUID, Annotated[str, Query(min_length=2, max_length=10)]]
    question: UUID
    right_answ_item: UUID
    item_text_2: Annotated[str, Query(min_length=2, max_length=255)]
    item_author_2: UUID
    context_2_id_sn: tuple[UUID, Annotated[str, Query(min_length=2, max_length=10)]]
    is_active: bool


class UpdateItemRelationViewRequest(BaseModel):
    pass
