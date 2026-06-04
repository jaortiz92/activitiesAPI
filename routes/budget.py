# FastAPI
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# APP
from .utils import get_db
from schemas.budget import (
    BudgetGroupSchema, BudgetGroupCreate,
    BudgetValueSchema, BudgetValueCreate,
    BudgetComparisonItem
)
import services.budget as service
from typing import List

budget = APIRouter(
    prefix="/budget",
    tags=["budget"]
)


@budget.get("/groups", response_model=List[BudgetGroupSchema])
def read_budget_groups(db: Session = Depends(get_db)):
    return service.get_budget_groups(db)


@budget.post("/groups", response_model=BudgetGroupSchema)
def create_budget_group(budget_group: BudgetGroupCreate, db: Session = Depends(get_db)):
    return service.create_budget_group(db, budget_group)


@budget.post("/values", response_model=BudgetValueSchema)
def create_budget_value(budget_value: BudgetValueCreate, db: Session = Depends(get_db)):
    return service.create_budget_value(db, budget_value)


@budget.get("/comparison", response_model=List[BudgetComparisonItem])
def get_comparison(month: int, year: int, mode: str = "monthly", db: Session = Depends(get_db)):
    return service.get_budget_comparison(db, month, year, mode)
