import datetime
from typing import Optional

from dateutil.parser import parse as date_parser

import utils.time_utils as time_utils
from model.scrap_type import ScrapType
from model.time_interval import TimeInterval


class SearchScrapParams:
    def __init__(
            self,
            search_by: str,
            scrap_from: datetime.datetime,
            scrap_to: datetime.datetime,
            language: Optional[str],
            scrap_series: str
    ):
        self._search_by = search_by
        self._scrap_from = time_utils.remove_microseconds_from_datetime(scrap_from)
        self._scrap_to = time_utils.remove_microseconds_from_datetime(scrap_to)
        self._type = ScrapType.SEARCH_BY
        self._scrap_series = scrap_series
        self._language = language if language is not None else 'None'
        return

    def get_search_by(self) -> str:
        return self._search_by

    def get_scrap_from(self) -> datetime.datetime:
        return self._scrap_from

    def get_scrap_to(self) -> datetime.datetime:
        return self._scrap_to

    def get_time_interval(self) -> TimeInterval:
        return TimeInterval(self._scrap_from, self._scrap_to)

    def get_type(self) -> ScrapType:
        return self._type

    def get_language(self) -> Optional[str]:
        return None if self._language == 'None' else self._language

    def get_scrap_series(self) -> str:
        return self._scrap_series

    @staticmethod
    def from_dict(dictionary):
        return SearchScrapParams(
            dictionary['_search_by'],
            date_parser(dictionary['_scrap_from']),
            date_parser(dictionary['_scrap_to']),
            dictionary['_language'],
            dictionary['_scrap_series']
        )
