from typing import Optional

import twint

import utils.docker_logs as docker_logs
from configuration.proxy_config import ProxyConfig
from model.hashtag_scrap_params import SearchScrapParams
from model.time_interval import TimeInterval
from model.user_scrap_params import ProfileTweetsScrapParams, ProfileDetailsScrapParams

logger = docker_logs.get_logger('scrap_service')


def get_common_config(
        interval: Optional[TimeInterval],
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
) -> twint.Config:
    twint_config = twint.Config()

    twint_config.Store_object = True
    twint_config.Hide_output = True

    if interval is not None:
        twint_config.Since = str(interval.get_start())
        twint_config.Until = str(interval.get_end())

    if proxy_config is not None:
        twint_config.Proxy_host = proxy_config.get_host()
        twint_config.Proxy_port = proxy_config.get_port()
        twint_config.Proxy_type = proxy_config.get_proxy_type()

    twint_config.Database = db_file_path

    return twint_config


def search_tweets(
        search_params: SearchScrapParams,
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
):
    logger.info('start scrap for search: ' + search_params.get_search_by())
    twint_config = get_common_config(search_params.get_time_interval(), db_file_path, proxy_config)
    twint_config.Search = search_params.get_search_by()
    if search_params.get_language() is not None:
        twint_config.Lang = search_params.get_language()
    twint.run.Search(twint_config)
    logger.info('finish scrap for search: ' + search_params.get_search_by())
    return


def get_user_details(
        params: ProfileDetailsScrapParams,
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
):
    logger.info('start scrap user details: ' + params.get_username())
    twint_config = get_common_config(None, db_file_path, proxy_config)
    twint_config.Username = params.get_username()
    twint_config.User_full = True
    logger.info('scrap user profile:   ' + params.get_username())
    twint.run.Lookup(twint_config)
    logger.info('scrap user followers: ' + params.get_username())
    twint.run.Followers(twint_config)
    logger.info('scrap user following: ' + params.get_username())
    twint.run.Following(twint_config)
    logger.info('scrap user favorites: ' + params.get_username())
    twint.run.Favorites(twint_config)
    logger.info('finish scrap user details: ' + params.get_username())
    return


def get_user_tweets(
        params: ProfileTweetsScrapParams,
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
):
    logger.info('start scrap for user: ' + params.get_username())
    twint_config = get_common_config(params.get_time_interval(), db_file_path, proxy_config)
    twint_config.Username = params.get_username()
    twint.run.Search(twint_config)
    logger.info('finish scrap for search: ' + params.get_username())
    return
