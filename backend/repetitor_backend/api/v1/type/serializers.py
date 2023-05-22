from pydantic import BaseModel, Field


class CustomerTypeResponce(BaseModel):
    pass


class CustomerTypeCreateRequest(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=200)
