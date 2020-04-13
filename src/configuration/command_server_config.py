import os

_command_server_host = os.environ['COMMAND_SERVER_HOST']


def get_command_server_host() -> str:
    return _command_server_host
