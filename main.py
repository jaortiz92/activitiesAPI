# FastApi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# App
from config import engine
from models import Base
from routes import (
    activity, account, transaction, category,
    description, kind, origin, query, budget
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url="/"
)

# Path Operations
app.include_router(transaction)
app.include_router(activity)
app.include_router(account)
app.include_router(category)
app.include_router(description)
app.include_router(kind)
app.include_router(origin)
app.include_router(query)
app.include_router(budget)

# CORS

origins = [
    "http://localhost",
    "http://127.0.0.1:8080",
    "http://192.168.0.3:8080",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://activity_fe:8080",
    "http://activity_be:8000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
