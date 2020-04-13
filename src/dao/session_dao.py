from typing import Optional

from utils.commands_mysql_utils import execute_sql_modify, execute_sql_query


def add_session(scrap_session_id: str, scrap_session_name: str):
    execute_sql_modify(
        '''INSERT INTO twint_distributed_tasks.ScrapSession(scrap_session_id, scrap_session_name) VALUE (%s, %s);''',
        [scrap_session_id, scrap_session_name])
    return


def get_scrap_session_id_by_name(scrap_session_name: str) -> Optional[str]:
    values = list(
        execute_sql_query(
            'SELECT * FROM twint_distributed_tasks.ScrapSession WHERE scrap_session_name=%s',
            [scrap_session_name]
        )['scrap_session_id'].to_numpy())
    return values[0] if len(values) > 0 else None


def get_scrap_session_name_by_id(scrap_session_name: str) -> Optional[str]:
    values = list(
        execute_sql_query(
            'SELECT * FROM twint_distributed_tasks.ScrapSession WHERE scrap_session_id=%s',
            [scrap_session_name]
        )['scrap_session_name'].to_numpy())
    return values[0] if len(values) > 0 else None


def get_not_finished_session_tasks_count(scrap_session_id: str) -> int:
    queries = [
        '''SELECT COUNT(*) FROM twint_distributed_tasks.SearchTweetScrapTasks 
        WHERE scrap_session_id=%s AND finished IS NULL''',
        '''SELECT COUNT(*) FROM twint_distributed_tasks.UserDetailsScrapTasks 
        WHERE scrap_session_id=%s AND finished IS NULL''',
        '''SELECT COUNT(*) FROM twint_distributed_tasks.UserTweetScrapTasks 
        WHERE scrap_session_id=%s AND finished IS NULL''',
        '''SELECT COUNT(*) FROM twint_distributed_tasks.UserFollowersScrapTasks 
        WHERE scrap_session_id=%s AND finished IS NULL''',
        '''SELECT COUNT(*) FROM twint_distributed_tasks.UserFollowingScrapTasks 
        WHERE scrap_session_id=%s AND finished IS NULL''',
        '''SELECT COUNT(*) FROM twint_distributed_tasks.UserFavoritesScrapTasks 
        WHERE scrap_session_id=%s AND finished IS NULL'''
    ]
    return sum([execute_sql_query(query, [scrap_session_id]).to_numpy()[0] for query in queries])


def get_all_sessions():
    return execute_sql_query('SELECT * FROM twint_distributed_tasks.ScrapSession', [])
