from typing import Optional

import twint

import utils.docker_logs as docker_logs
from configuration.proxy_config import ProxyConfig
from model.hashtag_scrap_params import PhraseScrapTaskParams
from model.time_interval import TimeInterval
from model.user_scrap_params import UserTweetsScrapTaskParams, UserDetailsScrapTaskParams
from utils.time_utils import remove_microseconds_from_datetime

logger = docker_logs.get_logger('scrap_service')


def get_common_config(
        interval: Optional[TimeInterval],
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
) -> twint.Config:
    twint_config = twint.Config()

    twint_config.Store_object = False
    twint_config.Hide_output = True
    twint_config.Retries_count = 100
    twint_config.Min_wait_time = 90
    twint_config.Backoff_exponent = 3.0

    if interval is not None:
        twint_config.Since = str(remove_microseconds_from_datetime(interval.since))
        twint_config.Until = str(remove_microseconds_from_datetime(interval.until))

    if proxy_config is not None:
        twint_config.Proxy_host = proxy_config.get_host()
        twint_config.Proxy_port = proxy_config.get_port()
        twint_config.Proxy_type = proxy_config.get_proxy_type()

    twint_config.Database = db_file_path

    return twint_config


def search_tweets(
        search_params: PhraseScrapTaskParams,
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
):
    logger.info('start scrap for search: ' + search_params.phrase)
    twint_config = get_common_config(search_params.get_time_interval(), db_file_path, proxy_config)
    twint_config.Search = search_params.phrase
    if search_params.language is not None:
        twint_config.Lang = search_params.language
    twint.run.Search(twint_config)
    logger.info('finish scrap for search: ' + search_params.phrase)
    return


def get_user_details(
        params: UserDetailsScrapTaskParams,
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
):
    logger.info('start scrap user details: ' + params.username)
    twint_config = get_common_config(None, db_file_path, proxy_config)
    twint_config.Username = params.username
    twint.run.Lookup(twint_config)
    logger.info('finish scrap user details: ' + params.username)
    return


def get_user_favorites(
        params: UserDetailsScrapTaskParams,
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
):
    logger.info('start scrap user favorites: ' + params.username)
    twint_config = get_common_config(None, db_file_path, proxy_config)
    twint_config.Username = params.username
    twint.run.Favorites(twint_config)
    logger.info('finish scrap user favorites: ' + params.username)
    return


def get_user_followers(
        params: UserDetailsScrapTaskParams,
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
):
    logger.info('start scrap user followers: ' + params.username)
    twint_config = get_common_config(None, db_file_path, proxy_config)
    twint_config.Username = params.username
    twint.run.Followers(twint_config)
    logger.info('finish scrap user followers: ' + params.username)
    return


def get_user_following(
        params: UserDetailsScrapTaskParams,
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
):
    logger.info('start scrap user following: ' + params.username)
    twint_config = get_common_config(None, db_file_path, proxy_config)
    twint_config.Username = params.username
    twint.run.Following(twint_config)
    logger.info('finish scrap user following: ' + params.username)
    return


def get_user_tweets(
        params: UserTweetsScrapTaskParams,
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
):
    logger.info('start scrap for user: ' + params.username)
    twint_config = get_common_config(params.get_time_interval(), db_file_path, proxy_config)
    twint_config.Username = params.username
    twint.run.Search(twint_config)
    logger.info('finish scrap for search: ' + params.username)
    return
