from uuid import UUID
from pydantic import BaseModel, Field

from repetitor_backend import tables


class CustomerTypeResponse(BaseModel):
    id: UUID
    name: str = Field(max_length=50)
    description: str = Field(max_length=200)
    is_active: bool

    @staticmethod
    def from_DB_model(db_model: tables.CustomerType) -> "CustomerTypeResponse":
        """Get CustomerTypeResponce model from DB model tables.CustomerType."""

        return CustomerTypeResponse(
            id=db_model.id,
            name=db_model.name,
            description=db_model.description,
            is_active=db_model.is_active,
        )


class CustomerTypeCreateRequest(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=200)


class ContextTypeCreateRequest(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=200)


class ContextTypeResponse(BaseModel):
    id: UUID
    name: str = Field(max_length=50)
    description: str
    is_active: bool

    @staticmethod
    def from_DB_model(db_model: tables.ContextType) -> "ContextTypeResponse":
        """Get CustomerTypeResponce model from DB model tables.CustomerType."""

        return ContextTypeResponse(
            id=db_model.id,
            name=db_model.name,
            description=db_model.description,
            is_active=db_model.is_active,
        )
