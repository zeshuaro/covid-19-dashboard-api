from pydantic import BaseModel
from typing import List, Dict


class GlobalStats(BaseModel):
    cases: int
    deaths: int
    recovered: int
    active: int
    critical: int
    casesPerOneMillion: int
    deathsPerOneMillion: int
    tests: int
    testsPerOneMillion: int
    affectedCountries: int
    todayCases: int
    todayDeaths: int


class CountryStats(BaseModel):
    cases: int
    deaths: int
    recovered: int
    active: int
    critical: int
    casesPerOneMillion: int
    deathsPerOneMillion: int
    tests: int
    testsPerOneMillion: int


class WorldMapCountryData(BaseModel):
    id: str
    value: int


class WorldMapCountryTopN(BaseModel):
    country: str
    value: int


class WorldMapCountrySummary(BaseModel):
    maxValue: int
    top_n: List[WorldMapCountryTopN]
    data: List[WorldMapCountryData]


class WorldMapCountry(BaseModel):
    cases: WorldMapCountrySummary
    deaths: WorldMapCountrySummary
    recovered: WorldMapCountrySummary
    active: WorldMapCountrySummary
    critical: WorldMapCountrySummary
    casesPerOneMillion: WorldMapCountrySummary
    deathsPerOneMillion: WorldMapCountrySummary
    tests: WorldMapCountrySummary
    testsPerOneMillion: WorldMapCountrySummary


class SingleLineChartHistSummary(BaseModel):
    data: List[int]
    labels: List[str]
    total: int


class SingleLineChartHist(BaseModel):
    cases: SingleLineChartHistSummary
    deaths: SingleLineChartHistSummary
    recovered: SingleLineChartHistSummary


class BarChartRaceCountryHistSummary(BaseModel):
    labels: List[str]
    colors: Dict[str, str]
    data: Dict[str, List[int]]


class BarChartRaceCountryHist(BaseModel):
    cases: BarChartRaceCountryHistSummary
    deaths: BarChartRaceCountryHistSummary
    recovered: BarChartRaceCountryHistSummary


class LineChartCountryHistData(BaseModel):
    label: str
    color: str
    data: List[int]


class LineChartCountryHistSummary(BaseModel):
    labels: List[str]
    datasets: List[LineChartCountryHistData]


class LineChartCountryHist(BaseModel):
    cases: LineChartCountryHistSummary
    deaths: LineChartCountryHistSummary
    recovered: LineChartCountryHistSummary
