# Python
from datetime import date, datetime
from typing import Optional, List, Dict

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# App
from .category import CategoryBase
from .description import DescriptionBase
from .kind import KindBase
from .origin import OriginBase
from .activity import ActivityShowFront, ActivityCompleteCreate, ActivityShowFront


class TransactionBase(BaseModel):
    transaction_date: date = Field(...)
    value: int = Field(..., gt=0, lt=100000000)
    detail: Optional[str] = Field(default=None)

    class Config:
        orm_mode = True


class TransactionCreate(TransactionBase):
    category_id: int = Field(..., gt=0)
    description_id: int = Field(..., gt=0)
    kind_id: int = Field(..., gt=0)
    origin_id: int = Field(..., gt=0)
    destiny_id: int = Field(..., gt=0)


class TransactionShow(TransactionCreate):
    transaction_id: int = Field(...)
    category: CategoryBase = Field(...)
    description: DescriptionBase = Field(...)
    kind: KindBase = Field(...)
    origin: OriginBase = Field(...)
    destiny: OriginBase = Field(...)
    activities: List[ActivityShowFront] = Field(...)
    created_date: datetime = Field(...)
    updated_date: Optional[datetime] = Field(...)


class TransactionCompleteCreate(TransactionCreate):
    activity_one: ActivityCompleteCreate = Field(...)
    activity_two: ActivityCompleteCreate = Field(...)


class TransactionShowFront(TransactionBase):
    transaction_id: int = Field(...)
    category: str = Field(...)
    description: str = Field(...)
    kind: str = Field(...)
    origin: str = Field(...)
    destiny: str = Field(...)
    activities: List[ActivityShowFront] = Field(...)
