import datetime
import json
import time

import pika

import configuration.proxy_config as proxy_config
import configuration.worker_config as worker_config
import scrap_service
import utils.docker_logs as docker_logs
import utils.tor_utils as tor_utils
from configuration import rabbit_config
from model.hashtag_scrap_params import SearchScrapParams
from model.scrap_type import ScrapType
from model.user_scrap_params import ProfileTweetsScrapParams, ProfileDetailsScrapParams
from upload_result_file_service import upload_result_file
from utils import command_utils

logger = docker_logs.get_logger('command_server')
tor_utils.prepare_tor()


def d2s(value: datetime.datetime) -> str:
    return str(value).replace(':', '').replace('-', '').replace(' ', '-')


def get_search_by_filename(params: SearchScrapParams) -> str:
    language_part = ('_lang=' + params.get_language()) if params.get_language() is not None else ''

    return 's__' + params.get_search_by() + '_' + d2s(params.get_scrap_from()) + '_' + d2s(
        params.get_scrap_to()) + language_part + '.db'


def get_user_tweets_filename(params: ProfileTweetsScrapParams) -> str:
    return 'ut__' + params.get_username() + '_' + d2s(params.get_scrap_from()) + '_' + d2s(
        params.get_scrap_to()) + '.db'


def get_user_profile_filename(params: ProfileDetailsScrapParams) -> str:
    return 'ud__' + params.get_username() + '.db'


def scrap_by_search_to_file(parsed_body):
    params = SearchScrapParams.from_dict(parsed_body)
    filename = get_search_by_filename(params)
    scrap_service.search_tweets(params, filename, proxy_config.default_proxy_config)
    return {
        'filename': filename,
        'series': parsed_body['_scrap_series'],
        'sub_series': 's_' + params.get_search_by(),
    }


def scrap_user_tweets_to_file(parsed_body):
    params: ProfileTweetsScrapParams = ProfileTweetsScrapParams.from_dict(parsed_body)
    filename = get_user_tweets_filename(params)
    scrap_service.get_user_tweets(params, filename, proxy_config.default_proxy_config)
    return {
        'filename': filename,
        'series': parsed_body['_scrap_series'],
        'sub_series': 'u_' + params.get_username(),
    }


def scrap_profile_details_to_file(parsed_body):
    params: ProfileDetailsScrapParams = ProfileDetailsScrapParams.from_dict(parsed_body)
    filename = get_user_profile_filename(params)
    scrap_service.get_user_details(params, filename, proxy_config.default_proxy_config)
    return {
        'filename': filename,
        'series': parsed_body['_scrap_series'],
        'sub_series': 'u_' + params.get_username(),
    }


def get_scrap_method(scrap_type: ScrapType):
    return {
        ScrapType.SEARCH_BY: scrap_by_search_to_file,
        ScrapType.USER_DETAILS: scrap_profile_details_to_file,
        ScrapType.USER_TWEETS: scrap_user_tweets_to_file
    }[scrap_type]


def process_message(ch, method, properties, body):
    print(" [x] Received %r" % body)
    body_string = body.decode("utf-8")
    parsed_body = json.loads(body_string)
    message_type: ScrapType = [it for it in ScrapType if it.__name__ == parsed_body['_type'].split('.')[-1]][0]
    logger.info('message_type: ' + str(message_type))

    try_count = 3
    is_success = False
    while not is_success and try_count > 0:
        try:
            logger.info('start new job for scrap user')
            logger.info('job_details: ' + body_string)
            scrap_result = get_scrap_method(message_type)(parsed_body)
            upload_result_file(
                series=scrap_result['series'],
                sub_series=scrap_result['sub_series'],
                filename=scrap_result['filename'],
                filepath=scrap_result['filename'],
                scrap_type=ScrapType.SEARCH_BY
            )
            command_utils.run_bash_command('rm ' + scrap_result['filename'])
            is_success = True
            logger.info('finished successful: ' + str(parsed_body))
        except Exception as exception:
            try_count = try_count - 1
            logger.error("Error during work")
            logger.exception(exception)
    if is_success:
        ch.basic_ack(method.delivery_tag)
    return


def prepare_rabbit_connect() -> pika.BlockingConnection:
    try_count = 100
    while try_count > 0:
        try:
            return pika.BlockingConnection(rabbit_config.get_rabbit_connection_config())
        except Exception:
            try_count = try_count - 1
            logger.error("error during connect to rabbitMQ")
            logger.error("wait 3 seconds for next try")
            time.sleep(3)
    raise Exception("can't connect with rabbitMQ")


connection = prepare_rabbit_connect()
channel = connection.channel()
channel.basic_qos(prefetch_count=2)

channel.queue_declare(queue=worker_config.get_queue_name(), durable=True)
channel.basic_consume(queue=worker_config.get_queue_name(), on_message_callback=process_message)

logger.info(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
