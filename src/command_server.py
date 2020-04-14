import time
from uuid import uuid4

from dateutil.parser import parse as date_parser
from flask import Flask
from flask import request, jsonify

import command_service
import utils.docker_logs as docker_logs
import utils.interval_utils as interval_utils
from model.scrap_type import ScrapType
from utils import commands_mysql_utils

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


def wait_for_mysql():
    try_count = 100
    success = False
    while try_count > 0 and not success:
        try:
            commands_mysql_utils.get_db_connection_base().close()
            success = True
        except Exception:
            try_count = try_count - 1
            logger.info("error during connect to mysql")
            logger.info("wait 3 seconds for next try")
            time.sleep(3)
    if success:
        return
    else:
        raise Exception("can't connect with mysql")


if __name__ == "__main__":
    wait_for_mysql()
    commands_mysql_utils.prepare_database()
    app.run(host="0.0.0.0", debug=True)
