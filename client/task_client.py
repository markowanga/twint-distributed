from datetime import datetime
from enum import Enum
from typing import Optional, Dict

import requests


class ScrapInterval(Enum):
    HOUR = 1
    DAY = 2
    MONTH = 3
    QUARTER_OF_YEAR = 4
    YEAR = 5

    def get_parameter_name(self) -> str:
        return {
            ScrapInterval.HOUR: 'hour',
            ScrapInterval.DAY: 'day',
            ScrapInterval.MONTH: 'month',
            ScrapInterval.QUARTER_OF_YEAR: 'quarter_of_year',
            ScrapInterval.YEAR: 'year'
        }[self]


class TwintDistributedTaskClient:
    """
    Client to add scrap tasks.

    interval_type -- this is interval time of subtask, big scrap task can be divided for smaller,
        it's better for scaling

    queue_name -- it's name of RabbitMQ queue, tasks can be adding to different queues

    scrap_series -- it can be group of tasks, when all tasks in group will be finished, the webhook with finish
        information will be send to parametrized host
    """

    def __init__(self, command_server_host):
        self.command_server_host = command_server_host
        return

    def add_user_tweets_to_scrap(self, username: str, interval_type: ScrapInterval, queue_name: str, scrap_series: str,
                                 since: Optional[datetime], until: Optional[datetime]):
        post_data = {
            'username': username,
            'interval_type': interval_type.get_parameter_name(),
            'queue_name': queue_name,
            'scrap_series': scrap_series,
            'since': since.isoformat() if since is not None else None,
            'until': until.isoformat() if since is not None else None
        }
        self.__call_post_request('/add_user_tweets_to_scrap', post_data)
        return

    def add_user_details_to_scrap(self, username: str, queue_name: str, scrap_series: str):
        post_data = {
            'username': username,
            'queue_name': queue_name,
            'scrap_series': scrap_series
        }
        self.__call_post_request('/add_user_details_to_scrap', post_data)
        return

    def add_user_followings_to_scrap(self, username: str, queue_name: str, scrap_series: str):
        post_data = {
            'username': username,
            'queue_name': queue_name,
            'scrap_series': scrap_series
        }
        self.__call_post_request('/add_user_followings_to_scrap', post_data)
        return

    def add_user_followers_to_scrap(self, username: str, queue_name: str, scrap_series: str):
        post_data = {
            'username': username,
            'queue_name': queue_name,
            'scrap_series': scrap_series
        }
        self.__call_post_request('/add_user_followers_to_scrap', post_data)
        return

    def add_user_favorites_to_scrap(self, username: str, queue_name: str, scrap_series: str):
        post_data = {
            'username': username,
            'queue_name': queue_name,
            'scrap_series': scrap_series
        }
        self.__call_post_request('/add_user_favorites_to_scrap', post_data)
        return

    def add_search_to_scrap(self, to_search: str, interval_type: ScrapInterval, queue_name: str, scrap_series: str,
                            since: Optional[datetime], until: Optional[datetime], language: Optional[str]):
        post_data = {
            'to_search': to_search,
            'interval_type': interval_type.get_parameter_name(),
            'queue_name': queue_name,
            'scrap_series': scrap_series,
            'since': since.isoformat() if since is not None else None,
            'until': until.isoformat() if since is not None else None,
            'language': language
        }
        self.__call_post_request('/add_search_to_scrap', post_data)
        return

    def __call_post_request(self, path: str, post_data: Dict[str, any]):
        url = self.command_server_host + path
        response = requests.post(url, data=post_data)
        if response.status_code >= 400:
            print("ERR path code:", response.status_code)
        return
