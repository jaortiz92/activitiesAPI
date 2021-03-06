# Python
from typing import List
from sqlalchemy.orm import Session

# App
import models
from models import Activity
import services
import schemas


def validate_foreign_keys(db: Session, activity: schemas.ActivityCreate):
    db_transaction: models.Transaction = services.get_transaction(
        db, activity.transaction_id)
    if not db_transaction:
        return "transaction"
    db_account: models.Account = services.get_account(db, activity.account_id)
    if not db_account:
        return "account"
    return None


def get_activity(db: Session, activity_id: int):
    db_activity: Activity = db.query(Activity).filter(
        Activity.activity_id == activity_id
    ).first()
    if db_activity:
        return db_activity
    return None


def get_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Activity).offset(skip).limit(limit).all()


def get_activities_by_transaction_id(db: Session, transaction_id: int):
    return db.query(Activity).filter(Activity.transaction_id == transaction_id).all()


def create_activity(db: Session, activity: schemas.ActivityCreate):
    validation = validate_foreign_keys(db, activity)
    if validation:
        return validation
    db_activity: Activity = Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def delete_activity(db: Session, activity_id: int):
    db_activity: Activity = get_activity(db, activity_id)
    if db_activity:
        db.delete(db_activity)
        db.commit()
        return f"Activity with activity_id {db_activity.activity_id} deleted"
    return None


def update_activity(db: Session, activity_id: int, activity: schemas.ActivityCreate):
    validation = validate_foreign_keys(db, activity)
    if validation:
        return validation
    db_activity = db.query(Activity).filter(
        Activity.activity_id == activity_id
    )
    if db_activity:
        db_activity.update(activity.dict())
        db.commit()
        return get_activity(db, activity_id)
    return None


def get_activities_by_transaction_show(db: Session, transaction_id: int):
    activities = get_activities_by_transaction_id(db, transaction_id)
    activities_dict = []
    for a in activities:
        activity = {
            "account_id": a.__dict__["account_id"],
            "activity_id": a.__dict__["activity_id"],
            "nature": a.__dict__["nature"]
        }
        activities_dict.append(activity)
    return activities_dict
