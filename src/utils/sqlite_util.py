import sqlite3

import pandas as pd

from utils.docker_logs import get_logger

logger = get_logger('sqlite_util')


def get_df_from_sqlite_db(db_filename: str, query: str):
    con = sqlite3.connect(db_filename)
    df = pd.read_sql_query(query, con)
    con.close()
    return df
