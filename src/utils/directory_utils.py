import os
from os import walk
from typing import List

import utils.command_utils as command_utils


def get_db_files_path_list_from_directory(directory_path: str) -> List[str]:
    db_files = []
    for (dirpath, dirnames, filenames) in walk(directory_path):
        db_files.extend([dirpath + '/' + it for it in filenames if '.db' in it])
    return db_files


def prepare_directory(directory: str):
    if not os.path.exists(directory):
        command_utils.run_bash_command('mkdir -p ' + directory)
    return
