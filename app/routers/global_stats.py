import requests

from collections import defaultdict
from fastapi import APIRouter

from app import const
from app.models.auth_models import *
from app.models.response_models import *

router = APIRouter()


@router.get(
    "/stats", summary="Global statistics", response_model=GlobalStats,
)
def get_global_stats():
    r = requests.get(const.BASE_URL + "/v2/all?yesterday=false")

    return r.json()
