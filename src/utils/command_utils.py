import os

import utils.docker_logs as docker_logs

command_logger = docker_logs.get_logger('command_runner')


def run_bash_command(command: str):
    command_logger.info('execute shell command: ' + command)
    os.system(command, )
    command_logger.info('finish executing: ' + command)
    return
