from typing import List

import pandas as pd

from configuration.mysql_config import get_db_connection, get_db_connection_base


def execute_sql_modify(query: str, params: List):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    return


def execute_sql_query(query: str, params: List = None):
    if params is None:
        params = list()
    connection = get_db_connection()
    df = pd.read_sql_query(query, connection, params=params)
    connection.close()
    return df


def is_db_initialized() -> bool:
    return 'twint_distributed_tasks' in list(
        pd.read_sql("SHOW DATABASES", get_db_connection_base())['Database'].to_numpy()
    )


def initialize_database():
    print('initialize_database start')
    connection = get_db_connection_base()
    cursor = connection.cursor()
    command = " ".join(open('utils/init_database.sql').readlines())
    print('command', command)
    cursor.execute(command)
    connection.commit()
    print('initialize_database finish')
    return


def prepare_database():
    if not is_db_initialized():
        print('database is not initialized')
        initialize_database()
    else:
        print('database is initialized')
    return
