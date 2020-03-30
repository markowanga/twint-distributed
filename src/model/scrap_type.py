from enum import Enum


class ScrapType(Enum):
    SEARCH_BY = 1
    USER_DETAILS = 2
    USER_TWEETS = 3
    USER_FOLLOWERS = 4
    USER_FOLLOWING = 5
    USER_FAVORITES = 6
