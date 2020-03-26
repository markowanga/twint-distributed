from flask import Flask
from flask import request, jsonify

import directory_tool

app = Flask(__name__)


def get_success_response():
    return jsonify({'status': 'SUCCESS'})


def get_directory_for_user(username: str) -> str:
    return '/data/user/u_' + username


def get_directory_for_hashtag(hashtag: str) -> str:
    return '/data/hashtag/h_' + hashtag


def get_path_for_user_database_file(username: str, filename: str) -> str:
    return get_directory_for_user(username) + '/' + filename


def get_path_for_hashtag_database_file(hashtag: str, filename: str) -> str:
    return get_directory_for_hashtag(hashtag) + '/' + filename


def prepare_hashtag_directory(hashtag: str):
    directory_tool.prepare_directory(get_directory_for_hashtag(hashtag))


def prepare_user_directory(username: str):
    directory_tool.prepare_directory(get_directory_for_user(username))


@app.route("/upload_user_db_file", methods=['POST'])
def upload_user_db_file():
    file = request.files['file']
    data = request.form
    username = data['username']
    filename = data['filename']
    prepare_user_directory(username)
    file.save(get_path_for_user_database_file(username, filename))
    return get_success_response()


@app.route("/upload_hashtag_db_file", methods=['POST'])
def upload_hashtag_db_file():
    file = request.files['file']
    data = request.form
    hashtag = data['hashtag']
    filename = data['filename']
    prepare_hashtag_directory(hashtag)
    file.save(get_path_for_hashtag_database_file(hashtag, filename))
    return get_success_response()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
