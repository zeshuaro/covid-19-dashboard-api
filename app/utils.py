import datetime as dt

from app import const


def parse_date(date):
    return dt.datetime.strptime(date, const.API_DATE_FMT)


def format_date(date):
    return date.strftime(const.DATE_FMT)
