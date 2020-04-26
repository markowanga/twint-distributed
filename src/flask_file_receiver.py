import pandas as pd
from flask import Flask, Response
from flask import request, jsonify

import utils.directory_utils as directory_utils
import utils.docker_logs as docker_logs
import utils.sqlite_util as sqlite_util

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
    db_file_path = ROOT_DATA_DIR + '/scrap_data/user_details' + '/' + user_folder_name + '/' + user_details_db_file
    df = sqlite_util.get_df_from_sqlite_db(db_file_path, 'SELECT * FROM users')
    return df_to_json_response(df)


@app.route("/get_user_tweets/<username>", methods=['GET'])
def get_user_tweets(username: str):
    since = request.args.get('since')
    until = request.args.get('until')
    return get_success_response()


@app.route("/get_phrase_tweets/<phrase>", methods=['GET'])
def get_phrase_tweets(phrase: str):
    # since = request.args.get('since')
    # until = request.args.get('until')
    logger.info('request tweets for phrase: ' + phrase)
    phrase_folder_name = 's_' + phrase
    base_directory_path = ROOT_DATA_DIR + '/scrap_data/search_by_phrase' + '/' + phrase_folder_name + '/'
    db_files = directory_utils.get_db_files_path_list_from_directory(base_directory_path)
    merged_data_df = pd.concat([
        sqlite_util.get_df_from_sqlite_db(db_file, 'SELECT * FROM tweets')
        for db_file in db_files
    ]).drop_duplicates(subset="id_str", keep=False)
    logger.info('rows count without duplicate: ' + str(merged_data_df.size))
    merged_data_df = merged_data_df.drop_duplicates(subset="id_str", keep=False)
    logger.info('rows count with duplicate: ' + str(merged_data_df.size))
    logger.info("/get_phrase_tweets -> df rows count: " + str(merged_data_df.size))
    logger.info("/get_phrase_tweets -> columns: " + str(merged_data_df.columns))
    logger.info("/get_phrase_tweets -> head log below")
    logger.info(merged_data_df.head())
    return df_to_json_response(merged_data_df)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
