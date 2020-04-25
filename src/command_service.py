from datetime import datetime
from typing import List, Optional
from uuid import uuid4

import pandas as pd
import requests
from pandas._libs.tslibs.nattype import NaT
from pandas._libs.tslibs.timestamps import Timestamp

import model.hashtag_scrap_params as hashtag_scrap_params
import utils.docker_logs as docker_logs
import utils.interval_utils as interval_utils
from configuration import webhook_config
from dao import user_favorites_task_dao, user_followings_task_dao, \
    user_followers_task_dao, user_details_task_dao, search_by_task_dao, user_tweets_task_dao, session_dao
from model.scrap_type import ScrapType
from model.time_interval import TimeInterval
from model.user_scrap_params import UserFavoritesScrapTaskParams, UserFollowersScrapTaskParams, \
    UserFollowingScrapTaskParams, \
    UserDetailsScrapTaskParams, UserTweetsScrapTaskParams
from utils.params_encoder import ParamsEncoder
from utils.rabbit_send_utils import send_to_rabbit

logger = docker_logs.get_logger('command_service')


def get_new_index() -> str:
    return str(uuid4())


def get_scrap_session_id_by_name(scrap_session_name: str) -> str:
    session_id = session_dao.get_scrap_session_id_by_name(scrap_session_name)
    if session_id is None:
        session_id = get_new_index()
        session_dao.add_session(session_id, scrap_session_name)
    return session_id


def get_interval_list(since: datetime, until: datetime,
                      interval_type: interval_utils.TimeIntervalType) -> List[TimeInterval]:
    return interval_utils.get_list_interval(since, until, interval_type)


def add_user_tweets_to_scrap(username: str, since: datetime, until: datetime, queue_name: str, scrap_series: str,
                             interval_type: interval_utils.TimeIntervalType):
    intervals = get_interval_list(since, until, interval_type=interval_type)
    since_non_null = sorted([it.since for it in intervals])[0]
    until_non_null = sorted([it.until for it in intervals])[-1]
    scrap_session_id = get_scrap_session_id_by_name(scrap_series)
    task_id = get_new_index()
    user_tweets_task_dao.add_task(task_id, username, since_non_null, until_non_null, datetime.now(), scrap_session_id,
                                  queue_name)
    for interval in get_interval_list(since=since, until=until, interval_type=interval_type):
        params = UserTweetsScrapTaskParams(
            task_id=get_new_index(),
            username=username,
            since=interval.since,
            until=interval.until,
            scrap_series=scrap_series,
            queue_name=queue_name
        )
        user_tweets_task_dao.add_sub_task(params.task_id, task_id, params.since, params.until, datetime.now())
        params_str = ParamsEncoder().default(params)
        logger.info(params_str + " " + params.queue_name)
        send_to_rabbit(params.queue_name, params_str)
    return


def add_user_details_to_scrap(username: str, queue_name: str, scrap_series: str):
    scrap_session_id = get_scrap_session_id_by_name(scrap_series)
    params = UserDetailsScrapTaskParams(
        task_id=get_new_index(),
        username=username,
        queue_name=queue_name,
        scrap_series=scrap_series
    )
    user_details_task_dao.add_task(params.task_id, username, datetime.now(), scrap_session_id, queue_name)
    params_str = ParamsEncoder().default(params)
    logger.info(params_str + " " + params.queue_name)
    send_to_rabbit(params.queue_name, params_str)
    return


def add_user_followings_to_scrap(username: str, queue_name: str, scrap_series: str):
    scrap_session_id = get_scrap_session_id_by_name(scrap_series)
    params = UserFollowingScrapTaskParams(
        task_id=get_new_index(),
        username=username,
        queue_name=queue_name,
        scrap_series=scrap_series
    )
    user_followings_task_dao.add_task(params.task_id, username, datetime.now(), scrap_session_id, queue_name)
    params_str = ParamsEncoder().default(params)
    logger.info(params_str + " " + queue_name)
    send_to_rabbit(queue_name, params_str)
    return


def add_user_followers_to_scrap(username: str, queue_name: str, scrap_series: str):
    scrap_session_id = get_scrap_session_id_by_name(scrap_series)
    params = UserFollowersScrapTaskParams(
        task_id=get_new_index(),
        username=username,
        queue_name=queue_name,
        scrap_series=scrap_series
    )
    user_followers_task_dao.add_task(params.task_id, username, datetime.now(), scrap_session_id, queue_name)
    params_str = ParamsEncoder().default(params)
    logger.info(params_str + " " + queue_name)
    send_to_rabbit(queue_name, params_str)
    return


def add_user_favorites_to_scrap(username: str, queue_name: str, scrap_series: str):
    scrap_session_id = get_scrap_session_id_by_name(scrap_series)
    params = UserFavoritesScrapTaskParams(
        task_id=get_new_index(),
        username=username,
        queue_name=queue_name,
        scrap_series=scrap_series
    )
    user_favorites_task_dao.add_task(params.task_id, username, datetime.now(), scrap_session_id, queue_name)
    params_str = ParamsEncoder().default(params)
    logger.info(params_str + " " + queue_name)
    send_to_rabbit(queue_name, params_str)
    return


def add_search_to_scrap(phrase: str, since: Optional[datetime], until: Optional[datetime], language: Optional[str],
                        queue_name: str, scrap_series: str, interval_type: interval_utils.TimeIntervalType):
    intervals = get_interval_list(since, until, interval_type=interval_type)
    since_non_null = sorted([it.since for it in intervals])[0]
    until_non_null = sorted([it.until for it in intervals])[-1]
    scrap_session_id = get_scrap_session_id_by_name(scrap_series)
    task_id = get_new_index()
    search_by_task_dao.add_task(task_id, phrase, since_non_null, until_non_null, datetime.now(), scrap_session_id,
                                queue_name)
    for interval in intervals:
        params = hashtag_scrap_params.PhraseScrapTaskParams(
            task_id=get_new_index(),
            phrase=phrase,
            since=interval.since,
            until=interval.until,
            language=language,
            queue_name=queue_name,
            scrap_series=scrap_series
        )
        search_by_task_dao.add_sub_task(params.task_id, task_id, params.since, params.until, datetime.now())
        params_str = ParamsEncoder().default(params)
        logger.info(params_str + " " + params.queue_name)
        send_to_rabbit(params.queue_name, params_str)
    return


def send_session_finished_webhook(scrap_session_name: str):
    post_data = {
        'scrap_session_name': scrap_session_name,
    }
    url = webhook_config.get_webhook_host() + '/scrap_session_finished'
    requests.post(url, data=post_data)
    return


def support_finish_session(session_id: str):
    count = session_dao.get_not_finished_session_tasks_count(session_id)
    if count == 0:
        session_name = session_dao.get_scrap_session_name_by_id(session_id)
        logger.info('finished session ' + session_name)
        if webhook_config.is_webhook_configured():
            send_session_finished_webhook(session_name)
        else:
            logger.info('webhook not configured')
    else:
        logger.info('count to finish session: ' + str(count))
    return


def set_task_as_finished(task_id: str, task_type: ScrapType):
    scrap_session_id = ''
    if task_type == ScrapType.USER_FAVORITES:
        user_favorites_task_dao.set_task_finished(task_id, datetime.now())
        scrap_session_id = user_favorites_task_dao.get_session_id(task_id)
    elif task_type == ScrapType.USER_FOLLOWINGS:
        user_followings_task_dao.set_task_finished(task_id, datetime.now())
        scrap_session_id = user_followings_task_dao.get_session_id(task_id)
    elif task_type == ScrapType.USER_FOLLOWERS:
        user_followers_task_dao.set_task_finished(task_id, datetime.now())
        scrap_session_id = user_followers_task_dao.get_session_id(task_id)
    elif task_type == ScrapType.USER_DETAILS:
        user_details_task_dao.set_task_finished(task_id, datetime.now())
        scrap_session_id = user_details_task_dao.get_session_id(task_id)
    else:
        raise Exception("Bad type")

    support_finish_session(scrap_session_id)
    return


def set_sub_task_as_finished(sub_task_id: str, task_type: ScrapType):
    if task_type == ScrapType.SEARCH_BY_PHRASE:
        dao = search_by_task_dao
    elif task_type == ScrapType.USER_TWEETS:
        dao = user_tweets_task_dao
    else:
        raise Exception("Bad type")

    task_id = dao.get_task_id_sub_task_id(sub_task_id)
    dao.set_sub_task_finished(sub_task_id, datetime.now())
    not_finished_sub_tasks_count = dao.get_all_not_finished_sub_tasks_by_task_id(task_id).size
    if not_finished_sub_tasks_count == 0:
        dao.set_task_finished(task_id, datetime.now())
        scrap_session_id = dao.get_session_id(task_id)
        support_finish_session(scrap_session_id)
    return


def map_value_to_string(value) -> Optional[any]:
    # print(value.__class__)
    if isinstance(value, Timestamp):
        print(value)
        return value.isoformat()
    elif value is NaT:
        return None
    else:
        return value


def data_frame_to_json_list(df: pd.DataFrame):
    df_list = [dict(row) for index, row in df.iterrows()]
    df_list = [
        {key: map_value_to_string(row[key]) for key in row.keys()}
        for row in df_list
    ]
    return df_list


def get_all_scrapped_tasks():
    df_dict = dict({
        ScrapType.SEARCH_BY_PHRASE.name: search_by_task_dao.get_all_tasks(),
        ScrapType.USER_FOLLOWERS.name: user_followers_task_dao.get_all_tasks(),
        ScrapType.USER_FOLLOWINGS.name: user_followings_task_dao.get_all_tasks(),
        ScrapType.USER_FAVORITES.name: user_favorites_task_dao.get_all_tasks(),
        ScrapType.USER_DETAILS.name: user_details_task_dao.get_all_tasks(),
        ScrapType.USER_TWEETS.name: user_tweets_task_dao.get_all_tasks()
    })
    return {it: data_frame_to_json_list(df_dict[it]) for it in df_dict.keys()}
