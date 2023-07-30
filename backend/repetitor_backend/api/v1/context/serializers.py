from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel


class ContextCreateRequest(BaseModel):
    name: Annotated[str, Query(min_length=1, max_length=50)]
    name_short: Annotated[str, Query(min_length=1, max_length=10)]
    context_type: UUID
    description: Annotated[str, Query(min_length=2, max_length=255)]
    is_active: bool = True


class ContextResponse(ContextCreateRequest):
    id: UUID


class UpdateContextRequest(BaseModel):
    # id: UUID
    name: Annotated[str | None, Query(min_length=1, max_length=50)]
    name_short: Annotated[str | None, Query(min_length=1, max_length=10)]
    context_type: UUID | None
    description: Annotated[str | None, Query(min_length=2, max_length=255)]
    is_active: bool = True
    pass


class GetContextRequest(UpdateContextRequest):
    id: UUID | None


class GetContextResponse(GetContextRequest):
    is_active: bool | None


class DeleteContextRequest(ContextResponse):
    pass
