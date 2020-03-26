import datetime


def date_to_string(date: datetime.date) -> str:
    return date.today().isoformat()


def remove_microseconds_from_datetime(value: datetime.datetime):
    return value.replace(microsecond=0)
