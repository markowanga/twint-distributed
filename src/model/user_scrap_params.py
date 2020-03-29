import datetime

from dateutil.parser import parse as date_parser

import utils.time_utils as time_utils
from model.time_interval import TimeInterval


class ProfileTweetsScrapParams:

    def __init__(self, username: str, scrap_from: datetime.datetime, scrap_to: datetime.datetime):
        self._username = username
        self._scrap_from = time_utils.remove_microseconds_from_datetime(scrap_from)
        self._scrap_to = time_utils.remove_microseconds_from_datetime(scrap_to)
        self._type = 'profile_tweets'
        return

    def get_username(self) -> str:
        return self._username

    def get_scrap_from(self) -> datetime.datetime:
        return self._scrap_from

    def get_scrap_to(self) -> datetime.datetime:
        return self._scrap_to

    def get_type(self) -> str:
        return self._type

    def get_time_interval(self) -> TimeInterval:
        return TimeInterval(self._scrap_from, self._scrap_to)

    @staticmethod
    def from_dict(dictionary):
        return ProfileTweetsScrapParams(
            dictionary['_username'],
            date_parser(dictionary['_scrap_from']),
            date_parser(dictionary['_scrap_to'])
        )


class ProfileDetailsScrapParams:

    def __init__(self, username: str):
        self._username = username
        self._type = 'profile_metadata'
        return

    def get_username(self) -> str:
        return self._username

    def get_type(self) -> str:
        return self._type

    @staticmethod
    def from_dict(dictionary):
        return ProfileTweetsScrapParams(
            dictionary['_username'],
            date_parser(dictionary['_scrap_from']),
            date_parser(dictionary['_scrap_to'])
        )
