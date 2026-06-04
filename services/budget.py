# SQLalchemy
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import date
import calendar

# APP
from models.budget import BudgetGroup, BudgetValue, BudgetGroupCategory
from models.activity import Activity
from models.transaction import Transaction
from models.account import Account
from models.classAccount import ClassAccount
from schemas.budget import BudgetGroupCreate, BudgetValueCreate


def get_budget_groups(db: Session):
    return db.query(BudgetGroup).all()


def create_budget_group(db: Session, budget_group: BudgetGroupCreate):
    db_group = BudgetGroup(name=budget_group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    for category_id in budget_group.account_ids:
        bg_category = BudgetGroupCategory(
            budget_group_id=db_group.budget_group_id, category_id=category_id)
        db.add(bg_category)

    db.commit()
    return db_group


def get_executed_amount(db: Session, budget_group_id: int, month: int, year: int, mode: str = "monthly"):
    # Get categories in the group
    categories = db.query(BudgetGroupCategory.category_id).filter(
        BudgetGroupCategory.budget_group_id == budget_group_id
    ).all()
    category_ids = [c[0] for c in categories]

    if not category_ids:
        return 0

    # Calculate date range
    last_day = calendar.monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    if mode == "ytd":
        start_date = date(year, 1, 1)
    else:
        start_date = date(year, month, 1)

    # Sum values of transactions associated with these categories
    # AND that have prefix 5, 6, or 7 in class_account
    total = db.query(func.sum(Transaction.value)).join(
        Activity, Activity.transaction_id == Transaction.transaction_id
    ).join(
        Account, Activity.account_id == Account.account_id
    ).join(
        ClassAccount, Account.class_account_id == ClassAccount.class_account_id
    ).filter(
        and_(
            Transaction.category_id.in_(category_ids),
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date,
            ClassAccount.class_account_id.in_((5, 6, 7))
        )
    ).scalar()

    return total or 0


def get_budget_comparison(db: Session, month: int, year: int, mode: str = "monthly"):
    groups = db.query(BudgetGroup).all()
    comparison = []

    for group in groups:
        # Budget amount for the year
        budget_val = db.query(BudgetValue).filter(
            BudgetValue.budget_group_id == group.budget_group_id,
            BudgetValue.year == year
        ).first()

        monthly_budget = budget_val.amount if budget_val else 0

        if mode == "ytd":
            budget_amount = monthly_budget * month
        else:
            budget_amount = monthly_budget

        executed_amount = get_executed_amount(
            db, group.budget_group_id, month, year, mode)

        comparison.append({
            "group_name": group.name,
            "budget_amount": budget_amount,
            "executed_amount": executed_amount,
            "variance": budget_amount - executed_amount
        })

    return comparison
