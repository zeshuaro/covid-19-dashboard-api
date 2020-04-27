import requests

from collections import defaultdict
from fastapi import APIRouter, Path, Query
from sortedcontainers import SortedList

from app import const, models

router = APIRouter()
STATS_TYPES = [
    "cases",
    "deaths",
    "recovered",
    "active",
    "critical",
    "casesPerOneMillion",
    "deathsPerOneMillion",
    "tests",
    "testsPerOneMillion",
]


@router.get(
    "/{query}/stats",
    summary="Country statistics for a specific country",
    response_model=models.CountryStats,
)
def get_country_stats(
    query: str = Path(
        ...,
        title="Query",
        description="Country Name or ISOs (ISO 2 | ISO 3) 3166 Country Standards",
        regex=r"^\w+(\s\w+)*$",
    )
):
    r = requests.get(
        const.BASE_URL + f"/v2/countries/{query}?yesterday=false&strict=true"
    )
    json = r.json()

    if r.status_code != 200:
        return json

    stats = {}
    for stats_type in STATS_TYPES:
        stats[stats_type] = json[stats_type]

    return stats


@router.get(
    "/world-map",
    summary="Country statistics for world map",
    response_model=models.WorldMapCountry,
)
def get_world_map(
    top_n: int = Query(
        5,
        title="Top N",
        description="The top n countries to retrieve additionally for each stats",
        ge=0,
    )
):
    r = requests.get(const.BASE_URL + "/v2/countries?yesterday=false")
    json = r.json()

    if r.status_code != 200:
        return json

    stats_types_extra = {"cases": "todayCases", "deaths": "todayDeaths"}
    max_values = defaultdict(int)
    stats = defaultdict(lambda: defaultdict(list))
    top_stats = defaultdict(lambda: SortedList(key=lambda x: -x["value"]))

    for country in json:
        iso3 = country["countryInfo"]["iso3"]
        if iso3 is None:
            iso3 = ""

        for stats_type in STATS_TYPES:
            value = country[stats_type]

            # Add the numbers for today as well
            if stats_type in stats_types_extra:
                value += country[stats_types_extra[stats_type]]

            stats[stats_type]["data"].append({"id": iso3, "value": value})
            top_stats[stats_type].add({"country": country["country"], "value": value})

            # Keep track of the maximum value
            if value > max_values[stats_type]:
                max_values[stats_type] = value
                stats[stats_type]["maxValue"] = value

            # Maintain the list of top n results
            if len(top_stats[stats_type]) > top_n:
                top_stats[stats_type].pop()

    # Append the list of top n results in the response
    for stats_type in STATS_TYPES:
        stats[stats_type]["top_n"] = list(top_stats[stats_type])

    return stats
