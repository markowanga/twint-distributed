import pandas as pd

import requests


class TwintDistributedDataClient:

    def __init__(self, data_server_host):
        self.data_server_host = data_server_host
        return

    def get_searched_tweets(self, to_search: str) -> pd.DataFrame:
        return self.__call_get_request('/get_searched_tweets/' + to_search)

    def get_user_tweets(self, username: str) -> pd.DataFrame:
        return self.__call_get_request('/get_user_tweets/' + username)

    def get_user_details(self, username: str) -> pd.DataFrame:
        return self.__call_get_request('/get_user_details/' + username)

    def get_user_followers(self, username: str) -> pd.DataFrame:
        return self.__call_get_request('/get_user_followers/' + username)

    def get_user_followings(self, username: str) -> pd.DataFrame:
        return self.__call_get_request('/get_user_followings/' + username)

    def get_user_favorites(self, username: str) -> pd.DataFrame:
        return self.__call_get_request('/get_user_favorites/' + username)

    def __call_get_request(self, path: str) -> pd.DataFrame:
        response = requests.get(self.data_server_host + requests.utils.quote(path))
        return pd.read_json(response.content)


def main():
    client = TwintDistributedDataClient('http://twitterdata.theliver.pl')
    users = ['AndrzejDuda', 'M_K_Blonska', 'pawel_tanajno', 'jakubiak_marek', 'mir_piotrowski', 'krzysztofbosak',
             'szymon_holownia', 'KosiniakKamysz', 'Grzywa_Slawomir', 'RobertBiedron', 'trzaskowski_']
    for user in users:
        responses = [
            client.get_user_tweets(user).sort_values(by='created_at')[['created_at']],
            # client.get_user_details(user),
            # client.get_user_followers(user),
            # client.get_user_followings(user),
            # client.get_user_favorites(user)
        ]
        print(user)
        print([it for it in responses])
    return


main()
