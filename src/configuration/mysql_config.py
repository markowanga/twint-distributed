import os

import mysql
from mysql.connector import MySQLConnection

db_hostname = os.environ['MYSQL_HOST']
db_port = os.environ['MYSQL_PORT']
db_username = os.environ['MYSQL_USER']
db_password = os.environ['MYSQL_PASSWORD']
TWINT_DISTRIBUTED_DATABASE = 'twint_distributed_tasks'


def get_db_connection() -> MySQLConnection:
    return mysql.connector.connect(
        host=db_hostname,
        port=db_port,
        user=db_username,
        passwd=db_password,
        database=TWINT_DISTRIBUTED_DATABASE
    )


def get_db_connection_base() -> MySQLConnection:
    return mysql.connector.connect(
        host=db_hostname,
        port=db_port,
        user=db_username,
        passwd=db_password
    )
