import datetime as dt
import json
import requests

from collections import defaultdict
from fastapi import APIRouter, Query, Path

from app import const, utils
from app.models.response_models import *
from app.routers import helpers

router = APIRouter()


@router.get(
    "/cumulative/bar-chart-race",
    summary="Cumulative country historical statistics for bar chart race",
    response_model=BarChartRaceCountryHist,
)
def get_bar_chart_race_cumulative(
    last_days: str = Query(
        "all",
        title="Last days",
        description="Number of days you want the data to go back to. Default is all. \
            Use all for full data set. Ex: 15, all, 24",
        regex=r"^(all)|\d+$",
    )
):
    return get_country_historical(last_days, const.BAR_CHART_RACE, is_new_stats=False)


@router.get(
    "/cumulative/line-chart",
    summary="Cumulative country historical statistics for line chart",
    response_model=LineChartCountryHist,
)
def get_grouped_line_chart_cumulative(
    last_days: str = Query(
        "all",
        title="Last days",
        description="Number of days you want the data to go back to. Default is all. \
            Use all for full data set. Ex: 15, all, 24",
        regex=r"^(all)|\d+$",
    ),
    top_n: int = Query(
        10, title="Top N", description="The top N results to be returned", gt=0
    ),
):
    return get_country_historical(
        last_days, const.LINE_CHART, is_new_stats=False, top_n=top_n
    )


@router.get(
    "/{query}/cumulative/line-chart",
    summary="Cumulative historical statistics for a specific country for line chart",
    response_model=SingleLineChartHist,
)
def get_single_line_chart_cumulative(
    query: str = Path(
        ...,
        title="Query",
        description="Country Name or ISOs (ISO 2 | ISO 3) 3166 Country Standards",
        regex=r"^\w+(\s\w+)*$",
    ),
    last_days: str = Query(
        "all",
        title="Last days",
        description="Number of days you want the data to go back to. Default is all. \
            Use all for full data set. Ex: 15, all, 24",
        regex=r"^(all)|\d+$",
    ),
):
    r = requests.get(const.BASE_URL + f"/v2/historical/{query}?lastdays={last_days}")
    json = r.json()

    if r.status_code != 200:
        return json

    return helpers.get_single_line_chart_hist(json["timeline"], is_new_stats=False)


@router.get(
    "/new/bar-chart-race",
    summary="New country historical statistics for bar chart race",
    response_model=BarChartRaceCountryHist,
)
def get_bar_chart_race_new(
    last_days: str = Query(
        "all",
        title="Last days",
        description="Number of days you want the data to go back to. Default is all. \
            Use all for full data set. Ex: 15, all, 24",
        regex=r"^(all)|\d+$",
    )
):
    return get_country_historical(last_days, const.BAR_CHART_RACE, is_new_stats=True)


@router.get(
    "/new/line-chart",
    summary="New country historical statistics for line chart",
    response_model=LineChartCountryHist,
)
def get_grouped_line_chart_new(
    last_days: str = Query(
        "all",
        title="Last days",
        description="Number of days you want the data to go back to. Default is all. \
            Use all for full data set. Ex: 15, all, 24",
        regex=r"^(all)|\d+$",
    ),
    top_n: int = Query(
        10, title="Top N", description="The top N results to be returned", gt=0
    ),
):
    return get_country_historical(
        last_days, const.LINE_CHART, is_new_stats=True, top_n=top_n
    )


@router.get(
    "/{query}/new/line-chart",
    summary="New historical statistics for a specific country for line chart",
    response_model=SingleLineChartHist,
)
def get_single_line_chart_new(
    query: str = Path(
        ...,
        title="Query",
        description="Country Name or ISOs (ISO 2 | ISO 3) 3166 Country Standards",
        regex=r"^\w+(\s\w+)*$",
    ),
    last_days: str = Query(
        "all",
        title="Last days",
        description="Number of days you want the data to go back to. Default is all. \
            Use all for full data set. Ex: 15, all, 24",
        regex=r"^(all)|\d+$",
    ),
):
    r = requests.get(const.BASE_URL + f"/v2/historical/{query}?lastdays={last_days}")
    json = r.json()

    if r.status_code != 200:
        return json

    return helpers.get_single_line_chart_hist(json["timeline"], is_new_stats=True)


def get_country_historical(last_days, chart_type, is_new_stats=True, top_n=None):
    """Get country historical statistics
    
    Arguments:
        last_days {int} -- The last n days of statistics to retrieve
        chart_type {int} -- The chart type
    
    Keyword Arguments:
        is_new_stats {bool} -- Whether to retrieve new or cumulative statistics 
            (default: {True})
        top_n {int} -- The top n results to retrieve (default: {None})
    
    Returns:
        dict -- The API response
    """
    r = requests.get(const.BASE_URL + f"/v2/historical?lastdays={last_days}")
    data = r.json()

    if r.status_code != 200:
        return data

    country_stats, dates = get_country_stats(data, top_n)
    stats = get_response_stats(country_stats, dates, chart_type, is_new_stats)

    return stats


def get_country_stats(data, top_n=None):
    """Get and aggregate statistics at a country level as 
        data is separated by state/province
    
    Arguments:
        data {dict} -- The API response
    
    Keyword Arguments:
        top_n {int} -- The top n results to retrieve (default: {None})
    
    Returns:
        dict -- The country statistics
    """
    stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    dates = defaultdict(set)
    date_obj = None

    for country in data:
        country_name = country["country"]
        country_timeline = country["timeline"]

        for stats_type in country_timeline:
            for date in country_timeline[stats_type]:
                date_obj = utils.parse_date(date)
                value = country_timeline[stats_type][date]

                stats[country_name][stats_type][date_obj] += value
                dates[stats_type].add(date_obj)

    if top_n is not None:
        stats = filter_country_stats(stats, top_n, date_obj)

    return stats, dates


def filter_country_stats(stats, top_n, latest_date):
    """Filter the top n country statistics
    
    Arguments:
        stats {dict} -- The country statistics
        top_n {int} -- The top n results to retrieve
        latest_date {datetime} -- The latest date
    
    Returns:
        dict -- The filtered country statistics
    """
    # Latest date should be returned by the API, if not,
    # Set the latest date to be the previous day
    if latest_date is None:
        now = dt.datetime.now()
        latest_date = dt.datetime(now.year, now.month, (now - dt.timedelta(days=1).day))

    # Get the total number of each statistics for each country
    totals = defaultdict(dict)
    for country in stats:
        for stats_type in stats[country]:
            totals[stats_type][country] = stats[country][stats_type][latest_date]

    # Get the top n results
    filtered_stats = defaultdict(dict)
    for stats_type in totals:
        sorted_kv = sorted(totals[stats_type].items(), key=lambda x: x[1], reverse=True)
        for country, _ in sorted_kv[:top_n]:
            filtered_stats[country][stats_type] = stats[country][stats_type]

    return filtered_stats


def get_response_stats(country_stats, dates, chart_type, is_new_stats):
    """Transform the country statistics into final API response
    
    Arguments:
        country_stats {dict} -- The country statistics
        dates {dict} -- The set of dates for each statistics
        chart_type {int} -- The chart type
        is_new_stats {bool} -- Whether to retrieve new or cumulative statistics
    
    Raises:
        ValueError: Invalid chart type
    
    Returns:
        dict -- The final API response
    """
    if chart_type == const.BAR_CHART_RACE:
        stats = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    elif chart_type == const.LINE_CHART:
        stats = defaultdict(dict)
    else:
        raise ValueError("Invalid chart type")

    with open("static/assets/colors.json") as f:
        colors = json.load(f)

    for stats_type in dates:
        line_chart_list = []
        sorted_dates = sorted(dates[stats_type])
        country_colors = {}

        for country in country_stats:
            # Filtering top n results can result in some statistics unavailable
            # for some countries, check if this is the case
            if stats_type not in country_stats[country]:
                continue

            last_value = 0
            line_chart_data = []

            for date_obj in sorted_dates:
                curr_value = country_stats[country][stats_type][date_obj]
                if is_new_stats:
                    new_value = curr_value - last_value
                    last_value = curr_value

                else:
                    new_value = curr_value

                if chart_type == const.BAR_CHART_RACE:
                    stats[stats_type]["data"][country].append(new_value)
                else:
                    line_chart_data.append(new_value)

            if country in colors["countries"]:
                color = colors["countries"][country]
            else:
                color = "#db5f57"

            if chart_type == const.BAR_CHART_RACE:
                country_colors[country] = color
            elif chart_type == const.LINE_CHART:
                line_chart_list.append(
                    {"label": country, "color": color, "data": line_chart_data,}
                )

        stats[stats_type]["labels"] = [utils.format_date(x) for x in sorted_dates]
        if chart_type == const.BAR_CHART_RACE:
            stats[stats_type]["colors"] = country_colors
        elif chart_type == const.LINE_CHART:
            stats[stats_type]["datasets"] = line_chart_list

    return stats
