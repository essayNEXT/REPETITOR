from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, validator
from pydantic.validators import datetime as pydantic_datetime


class CreateHelpRequest(BaseModel):
    text: Annotated[str, Query(min_length=2, max_length=255)]
    language: UUID
    front_name: Annotated[str, Query(min_length=2, max_length=255)]
    state: Annotated[str, Query(min_length=2, max_length=255)]
    auto_translation: bool | None = False
    positive_feedback: int | None = 0
    negative_feedback: int | None = 0
    total_impressions: int | None = 0

    @validator("total_impressions", pre=True)
    def validate_total_impressions(cls, total_impressions, values):
        positive_feedback = values.get("positive_feedback", 0)
        negative_feedback = values.get("negative_feedback", 0)
        expected_total_impressions = positive_feedback + negative_feedback
        if total_impressions < expected_total_impressions:
            raise ValueError(
                f"total_impressions should be equal to the sum of positive and negative feedbacks "
                f"(Expected: {expected_total_impressions}, Got: {total_impressions})"
            )
        return total_impressions


class UpdateHelpRequest(CreateHelpRequest):
    language: UUID | None = None
    state: str | None
    front_name: str | None
    is_active: bool = True


class GetHelpRequest(CreateHelpRequest):
    id: UUID | None
    text: str | None
    state: str | None
    front_name: str | None
    language: UUID | None
    is_active: bool | None
    modified_on: pydantic_datetime | None
    language__name_short: Annotated[str | None, Query(min_length=2, max_length=10)]


class GetHelpResponse(CreateHelpRequest):
    id: UUID
    modified_on: pydantic_datetime
    is_active: bool
