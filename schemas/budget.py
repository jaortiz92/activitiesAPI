# Pydantic
from pydantic import BaseModel
from typing import List, Optional

# Budget Group
class BudgetGroupBase(BaseModel):
    name: str

class BudgetGroupCreate(BudgetGroupBase):
    account_ids: List[int]

class BudgetGroupSchema(BudgetGroupBase):
    budget_group_id: int

    class Config:
        from_attributes = True

# Budget Value
class BudgetValueBase(BaseModel):
    year: int
    amount: int

class BudgetValueCreate(BudgetValueBase):
    budget_group_id: int

class BudgetValueSchema(BudgetValueBase):
    budget_value_id: int
    budget_group_id: int

    class Config:
        from_attributes = True

# Budget Comparison
class BudgetComparisonItem(BaseModel):
    group_name: str
    budget_amount: int
    executed_amount: int
    variance: int

    class Config:
        from_attributes = True
