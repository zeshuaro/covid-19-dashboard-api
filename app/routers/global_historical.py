import datetime as dt
import requests

from collections import defaultdict
from fastapi import APIRouter

from app import const, utils
from app.routers import helpers
from app.models.response_models import *

router = APIRouter()


@router.get(
    "/cumulative/line-chart",
    summary="Cumulative global historical statistics for line chart",
    response_model=SingleLineChartHist,
)
def get_line_chart_cumulative():
    r = requests.get(const.BASE_URL + "/v2/historical/all?lastdays=all")
    json = r.json()

    if r.status_code != 200:
        return json

    return helpers.get_single_line_chart_hist(json, is_new_stats=False)


@router.get(
    "/new/line-chart",
    summary="New global historical statistics for line chart",
    response_model=SingleLineChartHist,
)
def get_line_chart_new():
    r = requests.get(const.BASE_URL + "/v2/historical/all?lastdays=all")
    json = r.json()

    if r.status_code != 200:
        return json

    return helpers.get_single_line_chart_hist(json, is_new_stats=True)
