# Python
from datetime import datetime, date
from typing import Dict, List, Optional

# FastApi
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import Body, Path, Query
from sqlalchemy.orm.session import Session

# App
# from schemas import Message, MessageCreate

from schemas import (
    TransactionCreate, TransactionShow,
    TransactionCompleteCreate, ActivityCreate,
    TransactionShowFront
)
import services
from .utils import (
    register_not_found, if_error_redirect_transaction,
    get_db, if_error_redirect_activity, validate_cr_and_db
)

transaction = APIRouter(
    prefix="/transaction",
    tags=["Transaction"],
)


@transaction.get(
    path="/",
    response_model=List[TransactionShow],
    status_code=status.HTTP_200_OK,
    summary="Show all transactions"
)
def show_all_transactions(
    transaction_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    description_id: Optional[int] = None,
    kind_id: Optional[int] = None,
    origin_id: Optional[int] = None,
    destiny_id: Optional[int] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    detail: Optional[str] = Query(
        default=None,
        min_length=3
    ),
    skip: Optional[int] = Query(
        default=0,
        ge=0,
        title="Skip",
        description="Take the until row for show"
    ),
    limit: Optional[int] = Query(
        default=100,
        ge=0,
        title="Limit",
        description="Row's number to show"
    ),
    db: Session = Depends(get_db)
):
    """
    Show all Activities

    This path operation show all activities in the app

    Paramters:
    - 

    Retrurns a json list with all activities, with the following keys
    transaction_date: date,
    - value: int,
    - detail: str,
    - transaction_id: int,
    - category: Category
    - description: Description
    - kind: Kind,
    - origin: Origin,
    - destiny: Destiny,
    - activities: [Activity],
    - created_date: datetime,
    - updated_date: datetime
    """
    return services.get_transactions(
        db,
        transaction_id=transaction_id,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id,
        description_id=description_id,
        kind_id=kind_id,
        origin_id=origin_id,
        destiny_id=destiny_id,
        min_value=min_value,
        max_value=max_value,
        detail=detail,
        skip=skip, limit=limit
    )


@transaction.get(
    path="/{transaction_id}/search",
    response_model=TransactionShow,
    status_code=status.HTTP_200_OK,
    summary="Show a transaction"
)
def show_a_transaction(
    transaction_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    """
    Show a Transaction

    This path operation show a transaction in the app

    Paramters:
    - Register path parameter
        - transaction_id: int

    Retrurns a json with a transaction, with the following keys
    transaction_date: date,
    - value: int,
    - detail: str,
    - transaction_id: int,
    - category: Category
    - description: Description
    - kind: Kind,
    - origin: Origin,
    - destiny: Destiny,
    - activities: [Activity],
    - created_date: datetime,
    - updated_date: datetime
    """
    response = services.get_transaction(db, transaction_id)
    if not response:
        register_not_found("Transaction")
    return response


@transaction.post(
    path="/post",
    response_model=TransactionShow,
    status_code=status.HTTP_201_CREATED,
    summary="Create a Transaction"
)
def create_a_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a Transaction

    This path operation register a transaction in the app

    Parameters:
    - Register body parameter
        - transaction_date: date,
        - value: int,
        - detail: str,
        - category_id: int,
        - description_id: int,
        - kind_id: int,
        - origin_id: int,
        - destiny_id: int

    Retrurns a json with a transaction, with the following keys
    - value: int,
    - detail: str,
    - transaction_id: int,
    - category: Category
    - description: Description
    - kind: Kind,
    - origin: Origin,
    - destiny: Destiny,
    - activities: [],
    - created_date: datetime,
    - updated_date: datetime
    """
    response = services.create_transaction(db, transaction)
    if_error_redirect_transaction(response)
    return response


@transaction.delete(
    path="/{transaction_id}/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete a Transaction",
)
def delete_a_transaction(
    transaction_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    """
    Delete a Transaction

    This path operation delete a transaction

    Parameters:
    - Register path parameter
        - transaction_id: int

    Return a json with information about deletion
    """
    query = services.get_activities_by_transaction_id(db, transaction_id)
    if len(query) > 0:
        for activity in query:
            services.delete_activity(db, activity.activity_id)
    response = services.delete_transaction(db, transaction_id)
    if not response:
        register_not_found("Transaction")
    return response


@transaction.put(
    path="/{transaction_id}/update",
    response_model=TransactionShow,
    status_code=status.HTTP_200_OK,
    summary="Update a Transaction"
)
def update_a_transaction(
    transaction_id: int = Path(..., gt=0),
    transaction: TransactionCreate = Body(...),
    db: Session = Depends(get_db)
):
    """
    Update a Transaction

    This path operation update a transaction in the app

    Parameters:
    - Register path parameter
        - transaction_id: int
    - Register body parameter
        - transaction_date: date,
        - value: int,
        - detail: str,
        - category_id: int,
        - description_id: int,
        - kind_id: int,
        - origin_id: int,
        - destiny_id: int

    Retrurns a json with a transaction, with the following keys
    - value: int,
    - detail: str,
    - transaction_id: int,
    - category: Category
    - description: Description
    - kind: Kind,
    - origin: Origin,
    - destiny: Destiny,
    - activities: [Activity],
    - created_date: datetime,
    - updated_date: datetime
    """
    response = services.update_transaction(db, transaction_id, transaction)
    if_error_redirect_transaction(response)
    return response


@transaction.post(
    path="/complete_post",
    response_model=TransactionShow,
    status_code=status.HTTP_200_OK,
    summary="Create a Transaction and Activites"
)
def create_an_transaction_and_activities(
    transactionComplete: TransactionCompleteCreate = Body(...),
    db: Session = Depends(get_db)
):
    """
    Create a Transaction and its Activites

    This path operation register a transaction and its activities in the app

    Parameters:
    - Register body parameter
        - transaction_date: date,
        - value: int,
        - detail: str,
        - category_id: int,
        - description_id: int,
        - kind_id: int,
        - origin_id: int,
        - destiny_id: int
        - activity_one: Activity
        - activity_two: Activity

    Retrurns a json with a transaction, with the following keys
    - value: int,
    - detail: str,
    - transaction_id: int,
    - category: Category
    - description: Description
    - kind: Kind,
    - origin: Origin,
    - destiny: Destiny,
    - activities: [Activity],
    - created_date: datetime,
    - updated_date: datetime
    """
    transactionComplete: Dict = transactionComplete.dict()
    activity_one = transactionComplete.pop("activity_one")
    activity_two = transactionComplete.pop("activity_two")
    validate_cr_and_db(activity_one, activity_two)

    transaction = TransactionCreate(**transactionComplete)
    response = create_a_transaction(transaction, db)
    transaction_id = response.transaction_id

    activity_one["transaction_id"] = transaction_id
    activity_one = ActivityCreate(
        **activity_one
    )
    response_activity_one = services.create_activity(db, activity_one)
    if isinstance(response_activity_one, str):
        services.delete_transaction(db, transaction_id)
        if_error_redirect_activity(response_activity_one)

    activity_two["transaction_id"] = transaction_id
    activity_two = ActivityCreate(
        **activity_two
    )
    response_activity_two = services.create_activity(db, activity_two)
    if isinstance(response_activity_two, str):
        services.delete_activity(db, response_activity_one.activity_id)
        services.delete_transaction(db, transaction_id)
        if_error_redirect_activity(response_activity_two)
    return services.get_transaction(db, transaction_id)


@transaction.get(
    path="/count",
    status_code=status.HTTP_200_OK,
    summary="Return number of Transactions"
)
def count_all_transactions(
    db: Session = Depends(get_db)
):
    """
    Return number of Transactions

    This path operation counts all transactions in the app

    Parameters:
    - None

    Retrurn a json con numbers of registers:
    - registers: int
    """
    return {"registers": services.count_transactions(db)}


@transaction.get(
    path="/transactionShowFront",
    response_model=List[TransactionShowFront],
    status_code=status.HTTP_200_OK,
    summary="Show all transactions to front"
)
def show_all_transactions_show(
    skip: Optional[int] = Query(
        default=0,
        ge=0,
        title="Skip",
        description="Take the until row for show"
    ),
    limit: Optional[int] = Query(
        default=100,
        ge=0,
        title="Limit",
        description="Row's number to show"
    ),
    db: Session = Depends(get_db)
):
    """
    Show all Transactions

    This path operation show all transactions in the app

    Paramters:
    - 

    Retrurns a json list with all transactions, with the following keys
    transaction_date: date,
    - value: int,
    - detail: str,
    - transaction_id: int,
    - category: str
    - description: str
    - kind: str,
    - origin: str,
    - destiny: str,
    - activities: [Activity],
    """
    return services.get_transactions_show(db, skip=skip, limit=limit)
