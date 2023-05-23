from uuid import UUID
from pydantic import BaseModel, Field

from repetitor_backend import tables


class CustomerTypeResponce(BaseModel):
    id: UUID
    name: str = Field(max_length=50)
    description: str = Field(max_length=200)
    is_active: bool

    @staticmethod
    def from_DB_model(db_model: tables.CustomerType) -> "CustomerTypeResponce":
        """Get CustomerTypeResponce model from DB model tables.CustomerType."""

        return CustomerTypeResponce(
            id=db_model.id,
            name=db_model.name,
            description=db_model.description,
            is_active=db_model.is_active,
        )


class CustomerTypeCreateRequest(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=200)
