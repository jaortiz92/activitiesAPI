# Pydantic
from pydantic import BaseModel
from pydantic import Field

# App
from .group import Group


class KindBase(BaseModel):
    kind: str = Field(...)

    class Config:
        orm_mode = True


class Kind(KindBase):
    kind_id: int = Field(...)
    group: Group = Field(...)
