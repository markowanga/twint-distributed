from enum import Enum


class ScrapType(Enum):
    SEARCH_BY_PHRASE = 1
    USER_DETAILS = 2
    USER_TWEETS = 3
    USER_FOLLOWERS = 4
    USER_FOLLOWINGS = 5
    USER_FAVORITES = 6
