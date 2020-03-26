import os

import docker_logs

command_logger = docker_logs.get_logger('command_runner')


def run_bash_command(command: str, hide_output: bool = False):
    command_logger.info('execute shell command: ' + command)
    os.system(command, )
    command_logger.info('finish executing: ' + command)
    return
