from pydantic import BaseModel


class CustomerTypeResponce(BaseModel):
    pass


class CustomerTypeCreateRequest(BaseModel):
    name: str
    description: str

 