import pandas as pd
from flask import Flask, Response
from flask import request, jsonify

import utils.directory_utils as directory_utils
import utils.docker_logs as docker_logs
import utils.sqlite_util as sqlite_util

logger = docker_logs.get_logger('data_server')

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
    logger.info('get_user_tweets ' + username + ' start read tweets')
    user_folder_name = 'u_' + username
    base_directory_path = ROOT_DATA_DIR + '/scrap_data/user_tweets' + '/' + user_folder_name + '/'
    db_files = directory_utils.get_db_files_path_list_from_directory(base_directory_path)
    merged_data_df = pd.concat([
        sqlite_util.get_df_from_sqlite_db(db_file, 'SELECT * FROM tweets')
        for db_file in db_files
    ])
    logger.info('get_user_tweets ' + username + ' processing finished')
    df_without_duplicates = merged_data_df.drop_duplicates(subset="id_str")
    return df_to_json_response(df_without_duplicates)


@app.route("/get_searched_tweets/<to_search>", methods=['GET'])
def get_searched_tweets(to_search: str):
    logger.info('get_searched_tweets ' + to_search + ' start read tweets')
    phrase_folder_name = 's_' + to_search
    base_directory_path = ROOT_DATA_DIR + '/scrap_data/search_by_phrase' + '/' + phrase_folder_name + '/'
    db_files = directory_utils.get_db_files_path_list_from_directory(base_directory_path)
    merged_data_df = pd.concat([
        sqlite_util.get_df_from_sqlite_db(db_file, 'SELECT * FROM tweets')
        for db_file in db_files
    ])
    logger.info('get_searched_tweets ' + to_search + ' start remove duplicates')
    df_without_duplicates = merged_data_df.drop_duplicates(subset="id_str")
    logger.info('get_searched_tweets ' + to_search + ' processing finished')
    return df_to_json_response(df_without_duplicates)


@app.route("/get_user_followers/<username>", methods=['GET'])
def get_user_followers(username: str):
    user_folder_name = 'u_' + username
    user_details_db_file = 'ufe_' + username + '.db'
    db_file_path = ROOT_DATA_DIR + '/scrap_data/user_followers' + '/' + user_folder_name + '/' + user_details_db_file
    df = sqlite_util.get_df_from_sqlite_db(db_file_path, 'SELECT * FROM followers_names')['user']
    return df_to_json_response(df)


@app.route("/get_user_followings/<username>", methods=['GET'])
def get_user_followings(username: str):
    user_folder_name = 'u_' + username
    user_details_db_file = 'ufi_' + username + '.db'
    db_file_path = ROOT_DATA_DIR + '/scrap_data/user_followings' + '/' + user_folder_name + '/' + user_details_db_file
    df = sqlite_util.get_df_from_sqlite_db(db_file_path, 'SELECT * FROM following_names')['user']
    return df_to_json_response(df)


@app.route("/get_user_favorites/<username>", methods=['GET'])
def get_user_favorites(username: str):
    user_folder_name = 'u_' + username
    user_details_db_file = 'ufa_' + username + '.db'
    db_file_path = ROOT_DATA_DIR + '/scrap_data/user_favorites' + '/' + user_folder_name + '/' + user_details_db_file
    df = sqlite_util.get_df_from_sqlite_db(db_file_path, 'SELECT * FROM favorites')['tweet_id']
    return df_to_json_response(df)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
