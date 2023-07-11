from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel


class RightAnswItemCreateRequest(BaseModel):
    relation: UUID
    item: UUID


class UpdateRightAnswItemRequest(BaseModel):
    relation: UUID
    item: UUID
    is_active: bool = True


class GetRightAnswItemRequest(UpdateRightAnswItemRequest):
    id: UUID | None
    item: UUID | None
    relation: UUID | None
    is_active: bool | None
    item__author: UUID | None
    item__context__name_short: Annotated[str | None, Query(min_length=2, max_length=10)]
    item__text: Annotated[str | None, Query(min_length=2, max_length=255)]


class GetRightAnswItemResponse(GetRightAnswItemRequest):
    is_active: bool | None
