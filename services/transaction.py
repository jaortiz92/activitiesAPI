# Python
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, text

# App
import models
from models import Transaction, Activity
import services
import schemas
from datetime import date


def validate_foreign_keys(db: Session, transaction: schemas.TransactionCreate):
    db_category: models.Category = services.get_category(
        db, transaction.category_id)
    if not db_category:
        return "category"
    db_description: models.Description = services.get_description(
        db, transaction.description_id)
    if not db_description:
        return "description"
    db_kind: models.Kind = services.get_kind(db, transaction.kind_id)
    if not db_kind:
        return "kind"
    db_origin: models.Origin = services.get_origin(db, transaction.origin_id)
    if not db_origin:
        return "origin"
    db_destiny: models.Origin = services.get_origin(db, transaction.destiny_id)
    if not db_destiny:
        return "destiny"
    return None


def get_transaction(db: Session, transaction_id: int):
    db_transaction: Transaction = db.query(Transaction).filter(
        Transaction.transaction_id == transaction_id).first()
    if db_transaction:
        return db_transaction
    return None


def get_transactions(
    db: Session, transaction_id: int,
    start_date: date, end_date: date,
    category_id: int, description_id: int, kind_id: int,
    origin_id: int, destiny_id,
    min_value: float, max_value: float, detail: str,
    skip: int, limit: int
):
    query = db.query(Transaction)
    if transaction_id:
        return query.filter(Transaction.transaction_id == transaction_id).all()

    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    if min_value:
        query = query.filter(Transaction.value >= min_value)
    if max_value:
        query = query.filter(Transaction.value <= max_value)
    if origin_id:
        query = query.filter(Transaction.origin_id == origin_id)
    if destiny_id:
        query = query.filter(Transaction.destiny_id == destiny_id)
    if kind_id:
        query = query.filter(Transaction.kind_id == kind_id)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    if description_id:
        query = query.filter(Transaction.description_id == description_id)
    if detail:
        query = query.filter(Transaction.detail.ilike(f"%{detail}%"))

    return query.order_by(
        Transaction.transaction_date.desc()
    ).order_by(
        Transaction.transaction_date.desc(),
        Transaction.transaction_id.desc()
    ).offset(skip).limit(limit).all()


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    validation = validate_foreign_keys(db, transaction)
    if validation:
        return validation
    db_transaction: Transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int):
    db_transaction: Transaction = services.get_transaction(db, transaction_id)
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
        return f"Transaction with transaction_id {db_transaction.transaction_id} deleted"
    return None


def update_transaction(db: Session, transaction_id: int, transaction: schemas.TransactionCreate):
    validation = validate_foreign_keys(db, transaction)
    if validation:
        return validation
    db_transaction = db.query(Transaction).filter(
        Transaction.transaction_id == transaction_id)
    if db_transaction:
        db_transaction.update(transaction.dict())
        db.commit()
        return get_transaction(db, transaction_id)
    return None


def count_transactions(db: Session):
    return db.query(func.count(Transaction.transaction_id)).scalar()


def get_transactions_show(db: Session, skip: int = 0, limit: int = 100):

    sql = ("SELECT * FROM transactions_with_activities_show "
           "ORDER BY transaction_date DESC, transaction_id DESC, nature DESC "
           f"LIMIT {limit * 2} OFFSET {skip * 2}")
    db_query = db.execute(
        text(sql)).all()
    result_query = []

    for index in range(0, len(db_query), 2):
        activities = [
            {
                "account_id": db_query[index][10],
                "activity_id": db_query[index][9],
                "nature": db_query[index][11]
            },
            {
                "account_id": db_query[index + 1][10],
                "activity_id": db_query[index + 1][9],
                "nature": db_query[index + 1][11]
            }
        ]

        result_query.append({
            "transaction_id": db_query[index][0],
            "transaction_date": db_query[index][1],
            "category": db_query[index][2],
            "description": db_query[index][3],
            "kind": db_query[index][4],
            "activities": activities,
            "origin": db_query[index][5],
            "destiny": db_query[index][6],
            "value": db_query[index][7],
            "detail": db_query[index][8],
        })

    return result_query
