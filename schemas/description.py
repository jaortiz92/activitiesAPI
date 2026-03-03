# Pydantic
from pydantic import BaseModel
from pydantic import Field

# App
from .group import Group


class DescriptionBase(BaseModel):
    description: str = Field(...)

    class Config:
        orm_mode = True


class Description(DescriptionBase):
    description_id: int = Field(...)
    group: Group = Field(...)
