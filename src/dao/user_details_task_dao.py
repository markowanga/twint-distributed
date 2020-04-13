from datetime import datetime

from utils.commands_mysql_utils import execute_sql_modify, execute_sql_query


def add_task(task_id: str, username: str, created: datetime, scrap_session_id: str, queue_name: str):
    execute_sql_modify(
        '''INSERT INTO twint_distributed_tasks.UserDetailsScrapTasks(task_id, username, created, finished,
         scrap_session_id, queue_name) VALUE (%s, %s, %s, %s, %s, %s);''',
        [task_id, username, created, None, scrap_session_id, queue_name])
    return


def set_task_finished(task_id: str, finished: datetime):
    execute_sql_modify(
        '''UPDATE twint_distributed_tasks.UserDetailsScrapTasks
        SET finished = %s
        WHERE task_id = %s''',
        [finished, task_id])
    return


def get_session_id(task_id: str) -> str:
    return execute_sql_query(
        'SELECT * FROM twint_distributed_tasks.UserDetailsScrapTasks WHERE task_id=%s',
        [task_id]
    )['scrap_session_id'].to_numpy()[0]


def get_all_by_username(username: str):
    return execute_sql_query(
        'SELECT * FROM twint_distributed_tasks.UserDetailsScrapTasks WHERE username=%s',
        [username]
    )


def get_all_tasks():
    return execute_sql_query(
        '''SELECT task_id, username, created, finished, queue_name, scrap_session_name
        FROM twint_distributed_tasks.UserDetailsScrapTasks t 
            JOIN twint_distributed_tasks.ScrapSession s ON t.scrap_session_id = s.scrap_session_id''',
        [])
