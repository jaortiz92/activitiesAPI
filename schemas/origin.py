# Pydantic
from pydantic import BaseModel
from pydantic import Field


class OriginBase(BaseModel):
    origin: str = Field(...)

    class Config:
        orm_mode = True


class Origin(OriginBase):
    origin_id: int = Field(...)
