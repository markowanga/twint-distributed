import datetime
from enum import Enum
from typing import List, Union

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

import utils.time_utils as time_utils

TWITTER_START_TIME = parse('2006-03-21 00:00:00')


class TimeIntervalType(Enum):
    HOUR = 1
    DAY = 2
    MONTH = 3
    QUARTER_OF_YEAR = 4
    YEAR = 5

    @staticmethod
    def get_from_string(value: str):
        return {
            'hour': TimeIntervalType.HOUR,
            'day': TimeIntervalType.DAY,
            'month': TimeIntervalType.MONTH,
            'quarter_of_year': TimeIntervalType.QUARTER_OF_YEAR,
            'year': TimeIntervalType.YEAR
        }[value]

    def get_relativedelta(self):
        return {
            TimeIntervalType.HOUR: relativedelta(hours=1),
            TimeIntervalType.DAY: relativedelta(days=1),
            TimeIntervalType.MONTH: relativedelta(months=1),
            TimeIntervalType.QUARTER_OF_YEAR: relativedelta(months=3),
            TimeIntervalType.YEAR: relativedelta(years=1)
        }[self]


class TimeInterval:
    def __init__(self, start: datetime.datetime = None, end: datetime.datetime = None):
        self._start = start
        self._end = end

    def get_start(self) -> datetime.datetime:
        return self._start

    def get_end(self) -> datetime.datetime:
        return self._end

    def __repr__(self):
        return "TimeInterval(start=" + str(self._start) + ", end=" + str(self._end) + ")"


def get_list_interval(
        start: Union[datetime.datetime, None],
        end: Union[datetime.datetime, None],
        interval_type: TimeIntervalType
) -> List[TimeInterval]:
    fixed_start = start if start is not None else TWITTER_START_TIME
    fixed_end = end if end is not None else time_utils.remove_microseconds_from_datetime(datetime.datetime.now())
    current_time = fixed_start
    intervals_to_return = []
    while current_time < fixed_end:
        interval_start_time = current_time
        current_time = current_time + interval_type.get_relativedelta()
        interval_end_time = current_time - relativedelta(seconds=1)
        intervals_to_return.append(TimeInterval(
            interval_start_time,
            interval_end_time if interval_end_time < fixed_end else fixed_end
        ))
    return intervals_to_return


print(len(get_list_interval(None, None, TimeIntervalType.HOUR)))
