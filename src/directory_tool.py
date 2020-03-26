import command_tool
import os


def prepare_directory(directory: str):
    if not os.path.exists(directory):
        command_tool.run_bash_command('mkdir -p ' + directory)
    return
