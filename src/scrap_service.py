from typing import Optional

import twint

import utils.docker_logs as docker_logs
from configuration.proxy_config import ProxyConfig
from model.hashtag_scrap_params import SearchScrapParams
from model.time_interval import TimeInterval

logger = docker_logs.get_logger('scrap_service')


def search_tweets(
        search_params: SearchScrapParams,
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
):
    logger.info('start scrap for search: ' + search_params.get_search_by())

    twint_config = twint.Config()
    twint_config.Search = search_params.get_search_by()
    twint_config.Store_object = True
    twint_config.Hide_output = True
    if search_params.get_language() is not None:
        twint_config.Lang = search_params.get_language()

    interval = search_params.get_time_interval()
    twint_config.Since = str(interval.get_start())
    twint_config.Until = str(interval.get_end())

    if proxy_config is not None:
        twint_config.Proxy_host = proxy_config.get_host()
        twint_config.Proxy_port = proxy_config.get_port()
        twint_config.Proxy_type = proxy_config.get_proxy_type()

    twint_config.Database = db_file_path
    twint.run.Search(twint_config)

    logger.info('finish scrap for search: ' + search_params.get_search_by())
    return


def get_user(
        username: str,
        interval: TimeInterval,
        db_file_path: str,
        proxy_config: Optional[ProxyConfig]
):
    pass


def get_user_tweets(

):
    pass
