import logging

from typing import List, Annotated
from uuid import UUID
from fastapi import APIRouter, Query

from repetitor_backend import tables
from .serializers import (
    ContextCreateRequest,
    ContextResponse,
    UpdateContextRequest,
    GetContextRequest,
)
from repetitor_backend.db.crud import context

logger = logging.getLogger()

router = APIRouter()


@router.post("/context/")
async def create_context(new_context: ContextCreateRequest) -> UUID:
    """Create a new type of customer.

    Parameters:
    - name: str, max lenght is 50 symbols, required
    - describe: str, max lenght is 200 symbols, required
    """
    return await context.create(**new_context.dict())


@router.get(
    "/context/",
    response_model=List[ContextResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_context(get_param_context: GetContextRequest) -> list[dict]:
    """Get list of Context according of "query" parameter"""
    results = await context.get(**get_param_context.dict())
    1 == 1
    if get_param_context.is_key_only:
        fin_result = [
            {"id": result.id} for result in results if isinstance(result, tables.Context)
        ]
    else:
        fin_result = [
            result.to_dict() for result in results if isinstance(result, tables.Context)
        ]
    return fin_result


@router.patch("/context/")
async def update_context(update_param_context: UpdateContextRequest) -> UUID | None:
    """Update Context according of "query" parameter"""

    results = await context.update(**update_param_context.dict())
    1 == 1
    return results


@router.delete("/context/")
async def delete_context(id_param: UUID) -> UUID | None:
    """Update Context according of "query" parameter"""

    return await context.delete(id_param)
