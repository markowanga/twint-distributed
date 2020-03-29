from typing import List

from dateutil.parser import parse as date_parser
from flask import Flask
from flask import request, jsonify

import model.hashtag_scrap_params as hashtag_scrap_params
import model.user_scrap_params as user_scrap_params
import utils.docker_logs as docker_logs
import utils.interval_utils as interval_utils
from model.time_interval import TimeInterval
from utils.params_encoder import ParamsEncoder

from utils.rabbit_send_utils import send_to_rabbit

logger = docker_logs.get_logger('command_server')
app = Flask(__name__)


def get_success_response():
    return jsonify({'status': 'SUCCESS'})


def get_interval_list() -> List[TimeInterval]:
    since = date_parser(request.form['since']) if 'since' in request.form else None
    until = date_parser(request.form['until']) if 'until' in request.form else None
    interval_type = interval_utils.TimeIntervalType.get_from_string(request.form['interval_type'])
    return interval_utils.get_list_interval(since, until, interval_type)


@app.route("/add_user_tweets_to_scrap", methods=['POST'])
def add_user_tweets_to_scrap():
    queue_name = request.form['queue_name']
    username = request.form['username']
    for interval in get_interval_list():
        params = user_scrap_params.ProfileTweetsScrapParams(username, interval.get_start(), interval.get_end())
        params_str = ParamsEncoder().default(params)
        logger.info(params_str + " " + queue_name)
        send_to_rabbit(queue_name, params_str)
    return get_success_response()


@app.route("/add_user_profile_to_scrap", methods=['POST'])
def add_user_profile_to_scrap():
    queue_name = request.form['queue_name']
    username = request.form['username']
    params = user_scrap_params.ProfileDetailsScrapParams(username)
    params_str = ParamsEncoder().default(params)
    logger.info(params_str + " " + queue_name)
    send_to_rabbit(queue_name, params_str)
    return get_success_response()


@app.route("/add_search_to_scrap", methods=['POST'])
def add_search_to_scrap():
    logger.info('add_search_to_scrap')
    queue_name = request.form['queue_name']
    to_search = request.form['to_search']
    language = request.form['language'] if 'language' in request.form else None
    intervals = get_interval_list()
    for interval in intervals:
        params = hashtag_scrap_params.SearchScrapParams(to_search, interval.get_start(), interval.get_end(), language,
                                                        queue_name)
        params_str = ParamsEncoder().default(params)
        logger.info(params_str + " " + queue_name)
        send_to_rabbit(queue_name, params_str)
    return get_success_response()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
