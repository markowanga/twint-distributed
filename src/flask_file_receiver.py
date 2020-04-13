from flask import Flask
from flask import request, jsonify

import utils.directory_utils as directory_utils
import utils.docker_logs as docker_logs

logger = docker_logs.get_logger('flask_file_receiver')

app = Flask(__name__)

ROOT_DATA_DIR = '/data'


def get_success_response():
    return jsonify({'status': 'SUCCESS'})


def get_data_to_save_directory(data_type: str, sub_series: str) -> str:
    return ROOT_DATA_DIR + '/scrap_data/' + data_type + '/' + sub_series


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
