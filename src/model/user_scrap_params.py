import datetime

from dateutil.parser import parse as date_parser

import utils.time_utils as time_utils
from model.scrap_type import ScrapType
from model.time_interval import TimeInterval


class UserTweetsScrapParams:

    def __init__(self, username: str, scrap_from: datetime.datetime, scrap_to: datetime.datetime, scrap_series: str):
        self._username = username
        self._scrap_from = time_utils.remove_microseconds_from_datetime(scrap_from)
        self._scrap_to = time_utils.remove_microseconds_from_datetime(scrap_to)
        self._type = ScrapType.USER_TWEETS
        self._scrap_series = scrap_series
        return

    def get_username(self) -> str:
        return self._username

    def get_scrap_from(self) -> datetime.datetime:
        return self._scrap_from

    def get_scrap_to(self) -> datetime.datetime:
        return self._scrap_to

    def get_type(self) -> ScrapType:
        return self._type

    def get_time_interval(self) -> TimeInterval:
        return TimeInterval(self._scrap_from, self._scrap_to)

    def get_scrap_series(self) -> str:
        return self._scrap_series

    @staticmethod
    def from_dict(dictionary):
        return UserTweetsScrapParams(
            dictionary['_username'],
            date_parser(dictionary['_scrap_from']),
            date_parser(dictionary['_scrap_to']),
            dictionary['_scrap_series']
        )


class UserDetailsScrapParams:

    def __init__(self, username: str, scrap_series: str):
        self._username = username
        self._type = ScrapType.USER_DETAILS
        self._scrap_series = scrap_series
        return

    def get_username(self) -> str:
        return self._username

    def get_type(self) -> ScrapType:
        return self._type

    def get_scrap_series(self) -> str:
        return self._scrap_series

    @staticmethod
    def from_dict(dictionary):
        return UserDetailsScrapParams(
            dictionary['_username'],
            dictionary['_scrap_series']
        )


class UserFollowersScrapParams:

    def __init__(self, username: str, scrap_series: str):
        self._username = username
        self._type = ScrapType.USER_FOLLOWERS
        self._scrap_series = scrap_series
        return

    def get_username(self) -> str:
        return self._username

    def get_type(self) -> ScrapType:
        return self._type

    def get_scrap_series(self) -> str:
        return self._scrap_series

    @staticmethod
    def from_dict(dictionary):
        return UserDetailsScrapParams(
            dictionary['_username'],
            dictionary['_scrap_series']
        )


class UserFollowingScrapParams:

    def __init__(self, username: str, scrap_series: str):
        self._username = username
        self._type = ScrapType.USER_FOLLOWING
        self._scrap_series = scrap_series
        return

    def get_username(self) -> str:
        return self._username

    def get_type(self) -> ScrapType:
        return self._type

    def get_scrap_series(self) -> str:
        return self._scrap_series

    @staticmethod
    def from_dict(dictionary):
        return UserDetailsScrapParams(
            dictionary['_username'],
            dictionary['_scrap_series']
        )


class UserFavoritesScrapParams:

    def __init__(self, username: str, scrap_series: str):
        self._username = username
        self._type = ScrapType.USER_FAVORITES
        self._scrap_series = scrap_series
        return

    def get_username(self) -> str:
        return self._username

    def get_type(self) -> ScrapType:
        return self._type

    def get_scrap_series(self) -> str:
        return self._scrap_series

    @staticmethod
    def from_dict(dictionary):
        return UserDetailsScrapParams(
            dictionary['_username'],
            dictionary['_scrap_series']
        )
