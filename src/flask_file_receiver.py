import sqlite3

import pandas as pd
from flask import Flask, Response
from flask import request, jsonify

import utils.directory_utils as directory_utils
import utils.docker_logs as docker_logs

logger = docker_logs.get_logger('flask_file_receiver')

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

ROOT_DATA_DIR = '/data'


def get_success_response():
    return jsonify({'status': 'SUCCESS'})


def get_data_to_save_directory(data_type: str, sub_series: str) -> str:
    return ROOT_DATA_DIR + '/scrap_data/' + data_type + '/' + sub_series


def df_to_json_response(df: pd.DataFrame) -> Response:
    return Response(
        df.to_json(orient="records", date_format='iso'),
        mimetype='application/json'
    )


@app.route("/upload_result_file", methods=['POST'])
def upload_result_file():
    file = request.files['file']
    data = request.form
    sub_series = data['sub_series']
    filename = data['filename']
    data_type = data['data_type']

    file_directory = get_data_to_save_directory(data_type, sub_series)
    file_path = file_directory + '/' + filename

    directory_utils.prepare_directory(file_directory)
    file.save(file_path)

    return get_success_response()


@app.route("/get_user_details/<username>", methods=['GET'])
def get_user_details(username: str):
    user_folder_name = 'u_' + username
    user_details_db_file = 'ud_' + username + '.db'
    con = sqlite3.connect(ROOT_DATA_DIR + '/scrap_data/user_details' + '/' + user_folder_name + '/' +
                          user_details_db_file)
    df = pd.read_sql_query("SELECT * from users", con)
    return df_to_json_response(df)


@app.route("/get_user_tweets/<username>", methods=['GET'])
def get_user_tweets(username: str):
    since = request.args.get('since')
    until = request.args.get('until')
    return get_success_response()


@app.route("/get_phrase_tweets/<phrase>", methods=['GET'])
def get_phrase_tweets(phrase: str):
    since = request.args.get('since')
    until = request.args.get('until')
    return get_success_response()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
