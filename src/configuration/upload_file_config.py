import os

_upload_file_host = os.environ['UPLOAD_FILE_HOST']


def get_upload_file_host() -> str:
    return _upload_file_host
