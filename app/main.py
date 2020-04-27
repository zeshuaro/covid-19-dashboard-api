import datetime as dt
import pycountry
import requests

from collections import defaultdict
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sortedcontainers import SortedList

from app.routers import (
    global_stats,
    country_stats,
    global_historical,
    country_historical,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# TODO: update origins for deployment
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(global_stats.router, prefix="/global", tags=["Global"])
app.include_router(
    global_historical.router, prefix="/global/historical", tags=["Global Historical"],
)
app.include_router(country_stats.router, prefix="/country", tags=["Country"])

app.include_router(
    country_historical.router,
    prefix="/country/historical",
    tags=["Country Historical"],
)
