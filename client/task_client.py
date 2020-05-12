from datetime import datetime
from typing import Optional, Dict

import requests


class TwintDistributedTaskClient:

    def __init__(self, command_server_host):
        self.command_server_host = command_server_host
        return

    def add_user_tweets_to_scrap(self, username: str, interval_type: str, queue_name: str, scrap_series: str,
                                 since: Optional[datetime], until: Optional[datetime]):
        post_data = {
            'username': username,
            'interval_type': interval_type,
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

    def add_search_to_scrap(self, to_search: str, interval_type: str, queue_name: str, scrap_series: str,
                            since: Optional[datetime], until: Optional[datetime], language: Optional[str]):
        post_data = {
            'to_search': to_search,
            'interval_type': interval_type,
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
