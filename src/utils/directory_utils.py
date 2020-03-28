import utils.command_utils as command_utils
import os


def prepare_directory(directory: str):
    if not os.path.exists(directory):
        command_utils.run_bash_command('mkdir -p ' + directory)
    return
