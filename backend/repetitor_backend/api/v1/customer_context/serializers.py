from uuid import UUID

from pydantic import BaseModel, validator
from pydantic.validators import datetime as p_datetime


# from datetime import datetime


class CustomerContextCreateRequest(BaseModel):
    customer: UUID
    context_1: UUID
    context_2: UUID

    # last_date: p_datetime = datetime.utcnow()
    # is_active: bool = True

    @validator("context_2")
    def validate_context_2(cls, value, values):
        if "context_1" in values and value == values["context_1"]:
            raise ValueError("context_2 must have a different value than context_1")
        return value


# class CustomerContextResponse(CustomerContextCreateRequest):
#     id: UUID


class UpdateCustomerContextRequest(BaseModel):
    customer: UUID
    context_1: UUID
    context_2: UUID
    is_active: bool = True
    pass


class GetCustomerContextRequest(UpdateCustomerContextRequest):
    id: UUID | None
    customer: UUID | None
    context_1: UUID | None
    context_2: UUID | None
    last_date: p_datetime | None
    is_active: bool | None


class GetCustomerContextResponse(GetCustomerContextRequest):
    is_active: bool | None


# class DeleteCustomerContextRequest(CustomerContextResponse):
#     pass
