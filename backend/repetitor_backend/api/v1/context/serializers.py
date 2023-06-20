from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel


class ContextCreateRequest(BaseModel):
    name: Annotated[str, Query(min_length=1, max_length=50)]
    name_short: Annotated[str, Query(min_length=1, max_length=10)]
    context_class: UUID
    description: Annotated[str, Query(min_length=2, max_length=255)]
    is_active: bool = True


class ContextResponse(ContextCreateRequest):
    id: UUID


class UpdateContextRequest(BaseModel):
    name: Annotated[str, Query(min_length=1, max_length=50)] = None
    name_short: Annotated[str, Query(min_length=1, max_length=10)] = None
    context_class: UUID = None
    description: Annotated[str, Query(min_length=2, max_length=255)] = None
    is_active: bool = True
    is_key_only: Annotated[
        bool, Query(description="if only 'id' is needed")
    ] = False  # якщо потрібно тільки самі
    pass


class GetContextRequest(UpdateContextRequest):
    id: UUID | None = None
    is_key_only: Annotated[
        bool, Query(description="if only 'id' is needed")
    ] = False  # якщо потрібно тільки самі

class DeleteContextRequest(ContextResponse):
    pass
