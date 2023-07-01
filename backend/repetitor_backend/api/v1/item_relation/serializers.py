from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel


class ItemRelationCreateRequest(BaseModel):
    author: UUID
    explanation: UUID
    type: UUID


class UpdateItemRelationRequest(BaseModel):
    author: UUID
    explanation: UUID
    type: UUID
    is_active: bool = True


class GetItemRelationRequest(UpdateItemRelationRequest):
    id: UUID | None
    author: UUID | None
    explanation: UUID | None
    type: UUID | None
    is_active: bool | None
    explanation__description: str | None
    type__name: str | None

class GetItemRelationResponse(GetItemRelationRequest):
    is_active: bool | None


# class DeleteItemRelationRequest(ItemRelationResponse):
#     pass
