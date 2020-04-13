from uuid import uuid4

from dateutil.parser import parse as date_parser
from flask import Flask
from flask import request, jsonify

import command_service
import utils.docker_logs as docker_logs
import utils.interval_utils as interval_utils
from model.scrap_type import ScrapType

logger = docker_logs.get_logger('command_server')
app = Flask(__name__)


def get_new_index() -> str:
    return str(uuid4())


def get_success_response():
    return jsonify({'status': 'SUCCESS'})


@app.route("/add_user_tweets_to_scrap", methods=['POST'])
def add_user_tweets_to_scrap():
    command_service.add_user_tweets_to_scrap(
        username=request.form['username'],
        since=date_parser(request.form['since']) if 'since' in request.form else None,
        until=date_parser(request.form['until']) if 'since' in request.form else None,
        queue_name=request.form['queue_name'],
        scrap_series=request.form['scrap_series'],
        interval_type=interval_utils.TimeIntervalType.get_from_string(request.form['interval_type'])
    )
    return get_success_response()


@app.route("/add_user_details_to_scrap", methods=['POST'])
def add_user_details_to_scrap():
    command_service.add_user_details_to_scrap(
        username=request.form['username'],
        queue_name=request.form['queue_name'],
        scrap_series=request.form['scrap_series']
    )
    return get_success_response()


@app.route("/add_user_followings_to_scrap", methods=['POST'])
def add_user_followings_to_scrap():
    command_service.add_user_followings_to_scrap(
        username=request.form['username'],
        queue_name=request.form['queue_name'],
        scrap_series=request.form['scrap_series']
    )
    return get_success_response()


@app.route("/add_user_followers_to_scrap", methods=['POST'])
def add_user_followers_to_scrap():
    command_service.add_user_followers_to_scrap(
        username=request.form['username'],
        queue_name=request.form['queue_name'],
        scrap_series=request.form['scrap_series']
    )
    return get_success_response()


@app.route("/add_user_favorites_to_scrap", methods=['POST'])
def add_user_favorites_to_scrap():
    command_service.add_user_favorites_to_scrap(
        username=request.form['username'],
        queue_name=request.form['queue_name'],
        scrap_series=request.form['scrap_series']
    )
    return get_success_response()


@app.route("/add_search_to_scrap", methods=['POST'])
def add_search_to_scrap():
    command_service.add_search_to_scrap(
        phrase=request.form['to_search'],
        since=date_parser(request.form['since']) if 'since' in request.form else None,
        until=date_parser(request.form['until']) if 'since' in request.form else None,
        language=request.form['language'] if 'language' in request.form else None,
        queue_name=request.form['queue_name'],
        scrap_series=request.form['scrap_series'],
        interval_type=interval_utils.TimeIntervalType.get_from_string(request.form['interval_type'])
    )
    return get_success_response()


@app.route("/set_task_as_finished", methods=['POST'])
def set_task_as_finished():
    logger.info(request.form)
    command_service.set_task_as_finished(request.form['task_id'], ScrapType[request.form['task_type']])
    return get_success_response()


@app.route("/set_sub_task_as_finished", methods=['POST'])
def set_sub_task_as_finished():
    logger.info(request.form)
    command_service.set_sub_task_as_finished(request.form['sub_task_id'], ScrapType[request.form['task_type']])
    return get_success_response()


@app.route("/get_all_tasks", methods=['GET'])
def get_all_scrapped_users():
    return jsonify(command_service.get_all_scrapped_tasks())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
