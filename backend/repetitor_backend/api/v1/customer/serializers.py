from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr

from repetitor_backend import tables


class CustomerResponse(BaseModel):
    id: UUID
    customer_class: UUID
    tlg_user_id: int
    tlg_language: str
    tlg_first_name: str
    tlg_user_name: str | None
    tlg_last_name: str | None
    native_language: str | None
    first_name: str | None
    last_name: str | None
    email: EmailStr | None
    is_active: bool

    @staticmethod
    def from_DB_model(db_model: tables.Customer) -> "CustomerResponse":
        """Get CustomerResponse model from DB model tables.Customer."""

        return CustomerResponse(
            id=db_model.id,
            customer_class=db_model.customer_class,
            tlg_user_id=db_model.tlg_user_id,
            tlg_language=db_model.tlg_language,
            tlg_user_name=db_model.tlg_user_name,
            tlg_first_name=db_model.tlg_first_name,
            tlg_last_name=db_model.tlg_last_name,
            native_language=db_model.native_language,
            first_name=db_model.first_name,
            last_name=db_model.last_name,
            email=db_model.email,
            is_active=db_model.is_active,
        )


class CustomerCreateRequest(BaseModel):
    customer_class: UUID
    tlg_user_id: int
    tlg_language: str = Field(max_length=10)
    tlg_first_name: str = Field(max_length=50)
    tlg_user_name: Optional[str] = Field(max_length=50)
    tlg_last_name: Optional[str] = Field(max_length=50)
    native_language: Optional[str] = Field(max_length=10)
    first_name: Optional[str] = Field(max_length=50)
    last_name: Optional[str] = Field(max_length=50)
    email: Optional[EmailStr]


class CustomerUpdateRequest(BaseModel):
    id: UUID
    customer_class: Optional[UUID]
    tlg_user_id: Optional[int]
    tlg_language: Optional[str] = Field(max_length=10)
    tlg_first_name: Optional[str] = Field(max_length=50)
    tlg_user_name: Optional[str] = Field(max_length=50)
    tlg_last_name: Optional[str] = Field(max_length=50)
    native_language: Optional[str] = Field(max_length=10)
    first_name: Optional[str] = Field(max_length=50)
    last_name: Optional[str] = Field(max_length=50)
    email: Optional[EmailStr]
    is_active: Optional[bool]
