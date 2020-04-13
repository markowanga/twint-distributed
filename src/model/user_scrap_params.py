import datetime
from dataclasses import dataclass

from dateutil.parser import parse as date_parser

import utils.time_utils as time_utils
from model.scrap_type import ScrapType
from model.time_interval import TimeInterval


@dataclass(frozen=True)
class UserTweetsScrapTaskParams:
    task_id: str
    username: str
    since: datetime.datetime
    until: datetime.datetime
    type: ScrapType
    scrap_series: str
    queue_name: str

    def __init__(
            self,
            task_id: str,
            username: str,
            since: datetime.datetime,
            until: datetime.datetime,
            scrap_series: str,
            queue_name: str
    ):
        object.__setattr__(self, 'task_id', task_id)
        object.__setattr__(self, 'username', username)
        object.__setattr__(self, 'since', time_utils.remove_microseconds_from_datetime(since))
        object.__setattr__(self, 'until', time_utils.remove_microseconds_from_datetime(until))
        object.__setattr__(self, 'type', ScrapType.USER_TWEETS)
        object.__setattr__(self, 'scrap_series', scrap_series)
        object.__setattr__(self, 'queue_name', queue_name)
        return

    def get_time_interval(self):
        return TimeInterval(self.since, self.until)

    @staticmethod
    def from_dict(dictionary):
        return UserTweetsScrapTaskParams(
            dictionary['task_id'],
            dictionary['username'],
            date_parser(dictionary['since']),
            date_parser(dictionary['until']),
            dictionary['scrap_series'],
            dictionary['queue_name']
        )


@dataclass(frozen=True)
class UserDetailsScrapTaskParams:
    task_id: str
    username: str
    scrap_series: str
    type: ScrapType
    queue_name: str

    def __init__(self, task_id: str, username: str, scrap_series: str, queue_name: str):
        object.__setattr__(self, 'task_id', task_id)
        object.__setattr__(self, 'username', username)
        object.__setattr__(self, 'scrap_series', scrap_series)
        object.__setattr__(self, 'type', ScrapType.USER_DETAILS)
        object.__setattr__(self, 'queue_name', queue_name)
        return

    @staticmethod
    def from_dict(dictionary):
        return UserDetailsScrapTaskParams(
            dictionary['task_id'],
            dictionary['username'],
            dictionary['scrap_series'],
            dictionary['queue_name']
        )


@dataclass(frozen=True)
class UserFollowersScrapTaskParams:
    task_id: str
    username: str
    scrap_series: str
    type: ScrapType
    queue_name: str

    def __init__(self, task_id: str, username: str, scrap_series: str, queue_name: str):
        object.__setattr__(self, 'task_id', task_id)
        object.__setattr__(self, 'username', username)
        object.__setattr__(self, 'scrap_series', scrap_series)
        object.__setattr__(self, 'type', ScrapType.USER_FOLLOWERS)
        object.__setattr__(self, 'queue_name', queue_name)
        return

    @staticmethod
    def from_dict(dictionary):
        return UserFollowersScrapTaskParams(
            dictionary['task_id'],
            dictionary['username'],
            dictionary['scrap_series'],
            dictionary['queue_name']
        )


@dataclass(frozen=True)
class UserFollowingScrapTaskParams:
    task_id: str
    username: str
    scrap_series: str
    type: ScrapType
    queue_name: str

    def __init__(self, task_id: str, username: str, scrap_series: str, queue_name: str):
        object.__setattr__(self, 'task_id', task_id)
        object.__setattr__(self, 'username', username)
        object.__setattr__(self, 'scrap_series', scrap_series)
        object.__setattr__(self, 'type', ScrapType.USER_FOLLOWINGS)
        object.__setattr__(self, 'queue_name', queue_name)
        return

    @staticmethod
    def from_dict(dictionary):
        return UserFollowingScrapTaskParams(
            dictionary['task_id'],
            dictionary['username'],
            dictionary['scrap_series'],
            dictionary['queue_name']

        )


@dataclass(frozen=True)
class UserFavoritesScrapTaskParams:
    task_id: str
    username: str
    scrap_series: str
    type: ScrapType
    queue_name: str

    def __init__(self, task_id: str, username: str, scrap_series: str, queue_name: str):
        object.__setattr__(self, 'task_id', task_id)
        object.__setattr__(self, 'username', username)
        object.__setattr__(self, 'scrap_series', scrap_series)
        object.__setattr__(self, 'type', ScrapType.USER_FAVORITES)
        object.__setattr__(self, 'queue_name', queue_name)
        return

    @staticmethod
    def from_dict(dictionary):
        return UserFavoritesScrapTaskParams(
            dictionary['task_id'],
            dictionary['username'],
            dictionary['scrap_series'],
            dictionary['queue_name']
        )
