import requests

from collections import defaultdict
from fastapi import APIRouter

from app import const, models

router = APIRouter()


@router.get("/stats", summary="Global statistics", response_model=models.GlobalStats)
def get_global_stats():
    r = requests.get(const.BASE_URL + "/v2/all?yesterday=false")

    return r.json()
