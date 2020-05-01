import datetime as dt
import jwt
import pycountry
import requests

from collections import defaultdict
from fastapi import FastAPI, Query, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from fastapi.staticfiles import StaticFiles
from jwt import PyJWTError
from passlib.context import CryptContext
from sortedcontainers import SortedList

from app.models.auth_models import *
from app.routers import (
    auth,
    global_stats,
    country_stats,
    global_historical,
    country_historical,
)
from app.routers.auth import get_current_active_user

app = FastAPI(title="COVID-19 Dashboard API")
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://zeshuaro.github.io",
    "https://zeshuaro.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Auth"])
app.include_router(
    global_stats.router,
    prefix="/global",
    tags=["Global"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    global_historical.router,
    prefix="/global/historical",
    tags=["Global Historical"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    country_stats.router,
    prefix="/country",
    tags=["Country"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    country_historical.router,
    prefix="/country/historical",
    tags=["Country Historical"],
    dependencies=[Depends(get_current_active_user)],
)
