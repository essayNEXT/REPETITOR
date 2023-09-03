from typing import Annotated
from uuid import UUID

from fastapi import Query, HTTPException
from pydantic import BaseModel, validator
from pydantic.validators import datetime as pydantic_datetime

from repetitor_backend.api.v1.context.serializers import GetContextResponse


class CreateHelpRequest(BaseModel):
    text: Annotated[str, Query(min_length=2, max_length=255)]
    language: UUID
    front_name: Annotated[str, Query(min_length=2, max_length=255)]
    state: Annotated[str, Query(min_length=2, max_length=255)]
    positive_feedback: int | None = 0
    negative_feedback: int | None = 0
    total_impressions: int | None = 0
    auto_translation: bool | None = False

    @validator("total_impressions", pre=True)
    def validate_total_impressions(cls, total_impressions, values):
        positive_feedback = values.get("positive_feedback", 0) or 0
        negative_feedback = values.get("negative_feedback", 0) or 0
        total_impressions_2 = total_impressions or 0
        expected_total_impressions = positive_feedback + negative_feedback
        if total_impressions_2 < expected_total_impressions:
            raise HTTPException(
                status_code=404,
                detail=f"total_impressions should be equal to the sum of positive and negative feedbacks "
                f"(Expected: {expected_total_impressions}, Got: {total_impressions})",
            )

        return total_impressions


class UpdateHelpRequest(CreateHelpRequest):
    text: str = None
    language: UUID = None
    front_name: str = None
    state: str = None
    total_impressions: int = None
    positive_feedback: int = None
    negative_feedback: int = None
    auto_translation: bool = None
    modified_on: pydantic_datetime = None
    is_active: bool = True
    modifying_total_impressions: int = None
    modifying_positive_feedback: int = None
    modifying_negative_feedback: int = None


class GetHelpRequest(CreateHelpRequest):
    id: UUID | None
    text: str | None
    state: str | None
    front_name: str | None
    language: UUID | None
    is_active: bool | None
    total_impressions: int | None
    positive_feedback: int | None
    negative_feedback: int | None
    auto_translation: bool | None
    modified_on: pydantic_datetime | None
    language__name_short: Annotated[str | None, Query(min_length=2, max_length=10)]

    def __init__(self, **data):
        super().__init__(**data)

        if all(v is None for v in self.dict().values()):
            self.language__name_short = "en"


class GetHelpResponse(BaseModel):
    id: UUID
    text: str
    language: GetContextResponse
    front_name: str
    state: str
    total_impressions: int
    positive_feedback: int
    negative_feedback: int
    auto_translation: bool
    modified_on: pydantic_datetime
    is_active: bool
