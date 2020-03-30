import datetime
import functools
import json
import threading
import time

import pika

import configuration.proxy_config as proxy_config
import scrap_service
import utils.docker_logs as docker_logs
import utils.tor_utils as tor_utils
from configuration import rabbit_config, worker_config
from model.hashtag_scrap_params import SearchScrapParams
from model.scrap_type import ScrapType
from model.user_scrap_params import UserTweetsScrapParams, UserDetailsScrapParams
from upload_result_file_service import upload_result_file
from utils import command_utils

logger = docker_logs.get_logger('command_server')
tor_utils.prepare_tor()


def d2s(value: datetime.datetime) -> str:
    return str(value).replace(':', '').replace('-', '').replace(' ', '-')


def get_search_by_filename(params: SearchScrapParams) -> str:
    language_part = ('_lang=' + params.get_language()) if params.get_language() is not None else ''

    return 's_' + params.get_search_by() + '_' + d2s(params.get_scrap_from()) + '_' + d2s(
        params.get_scrap_to()) + language_part + '.db'


def get_user_tweets_filename(params: UserTweetsScrapParams) -> str:
    return 'ut_' + params.get_username() + '_' + d2s(params.get_scrap_from()) + '_' + d2s(
        params.get_scrap_to()) + '.db'


def get_user_details_filename(params: UserDetailsScrapParams) -> str:
    return 'ud_' + params.get_username() + '.db'


def get_user_favorites_filename(params: UserDetailsScrapParams) -> str:
    return 'ufa_' + params.get_username() + '.db'


def get_user_followers_filename(params: UserDetailsScrapParams) -> str:
    return 'ufe_' + params.get_username() + '.db'


def get_user_following_filename(params: UserDetailsScrapParams) -> str:
    return 'ufi_' + params.get_username() + '.db'


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
    params: UserTweetsScrapParams = UserTweetsScrapParams.from_dict(parsed_body)
    filename = get_user_tweets_filename(params)
    scrap_service.get_user_tweets(params, filename, proxy_config.default_proxy_config)
    return {
        'filename': filename,
        'series': parsed_body['_scrap_series'],
        'sub_series': 'u_' + params.get_username(),
    }


def scrap_user_details_to_file(parsed_body):
    params: UserDetailsScrapParams = UserDetailsScrapParams.from_dict(parsed_body)
    filename = get_user_details_filename(params)
    scrap_service.get_user_details(params, filename, proxy_config.default_proxy_config)
    return {
        'filename': filename,
        'series': parsed_body['_scrap_series'],
        'sub_series': 'u_' + params.get_username(),
    }


def scrap_user_favorites_to_file(parsed_body):
    params: UserDetailsScrapParams = UserDetailsScrapParams.from_dict(parsed_body)
    filename = get_user_favorites_filename(params)
    scrap_service.get_user_favorites(params, filename, proxy_config.default_proxy_config)
    return {
        'filename': filename,
        'series': parsed_body['_scrap_series'],
        'sub_series': 'u_' + params.get_username(),
    }


def scrap_user_following_to_file(parsed_body):
    params: UserDetailsScrapParams = UserDetailsScrapParams.from_dict(parsed_body)
    filename = get_user_following_filename(params)
    scrap_service.get_user_following(params, filename, proxy_config.default_proxy_config)
    return {
        'filename': filename,
        'series': parsed_body['_scrap_series'],
        'sub_series': 'u_' + params.get_username(),
    }


def scrap_user_followers_to_file(parsed_body):
    params: UserDetailsScrapParams = UserDetailsScrapParams.from_dict(parsed_body)
    filename = get_user_followers_filename(params)
    scrap_service.get_user_followers(params, filename, proxy_config.default_proxy_config)
    return {
        'filename': filename,
        'series': parsed_body['_scrap_series'],
        'sub_series': 'u_' + params.get_username(),
    }


def get_scrap_method(scrap_type: ScrapType):
    return {
        ScrapType.SEARCH_BY: scrap_by_search_to_file,
        ScrapType.USER_DETAILS: scrap_user_details_to_file,
        ScrapType.USER_TWEETS: scrap_user_tweets_to_file,
        ScrapType.USER_FOLLOWING: scrap_user_following_to_file,
        ScrapType.USER_FOLLOWERS: scrap_user_followers_to_file,
        ScrapType.USER_FAVORITES: scrap_user_favorites_to_file
    }[scrap_type]


def ack_message(ch, delivery_tag):
    """Note that `ch` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if ch.is_open:
        ch.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass


def process_message(body):
    logger.info(" [x] Received %r" % body)
    time.sleep(500)
    body_string = body.decode("utf-8")
    parsed_body = json.loads(body_string)
    message_type: ScrapType = [it for it in ScrapType if parsed_body['_type'] in str(it)][0]
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
                scrap_type=message_type
            )
            command_utils.run_bash_command('rm ' + scrap_result['filename'])
            is_success = True
            logger.info('finished successful: ' + str(parsed_body))
        except Exception as exception:
            try_count = try_count - 1
            logger.error("Error during work")
            logger.exception(exception)
    return


def do_work(conn, ch, delivery_tag, body):
    thread_id = threading.get_ident()
    logger.info('Thread id: %s Delivery tag: %s Message body: %s', thread_id, delivery_tag, body)
    process_message(body)
    cb = functools.partial(ack_message, ch, delivery_tag)
    conn.add_callback_threadsafe(cb)
    return


def prepare_rabbit_connect() -> pika.BlockingConnection:
    try_count = 100
    while try_count > 0:
        try:
            return pika.BlockingConnection(rabbit_config.get_rabbit_connection_config())
        except Exception:
            try_count = try_count - 1
            logger.info("error during connect to rabbitMQ")
            logger.info("wait 3 seconds for next try")
            time.sleep(3)
    raise Exception("can't connect with rabbitMQ")


def on_message(ch, method_frame, _header_frame, body, args):
    (conn, thrds) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(conn, ch, delivery_tag, body))
    t.start()
    thrds.append(t)


connection = prepare_rabbit_connect()
channel = connection.channel()

channel.exchange_declare(
    exchange="test_exchange",
    exchange_type="direct",
    passive=False,
    durable=True,
    auto_delete=False)
channel.queue_declare(queue=worker_config.get_queue_name(), durable=True)
# channel.queue_bind(queue=worker_config.get_queue_name())
# Note: prefetch is set to 1 here as an example only and to keep the number of threads created
# to a reasonable amount. In production you will want to test with different prefetch values
# to find which one provides the best performance and usability for your solution
channel.basic_qos(prefetch_count=1)

threads = []
on_message_callback = functools.partial(on_message, args=(connection, threads))
channel.basic_consume(queue=worker_config.get_queue_name(), on_message_callback=on_message_callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

# Wait for all to complete
for thread in threads:
    thread.join()
