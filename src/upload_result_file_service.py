import requests

import configuration.upload_file_config as upload_file_config
import utils.docker_logs as docker_logs
from model.scrap_type import ScrapType

logger = docker_logs.get_logger('upload_result_file_service')


def upload_result_file(
        series: str,
        sub_series: str,
        filename: str,
        filepath: str,
        scrap_type: ScrapType
):
    post_data = {
        'series': series,
        'sub_series': sub_series,
        'filename': filename,
        'data_type': scrap_type.name.lower()
    }
    url = 'http://' + upload_file_config.get_upload_file_host() + '/upload_result_file'
    post_files = {'file': open(filepath, 'rb')}
    response = requests.post(url, data=post_data, files=post_files)
    logger.info('upload request response with code: ' + str(response.status_code))
    return
