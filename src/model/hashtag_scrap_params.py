import datetime
from dataclasses import dataclass
from typing import Optional

from dateutil.parser import parse as date_parser

import utils.time_utils as time_utils
from model.scrap_type import ScrapType
from model.time_interval import TimeInterval


@dataclass(frozen=True)
class PhraseScrapTaskParams:
    task_id: str
    phrase: str
    since: datetime.datetime
    until: datetime.datetime
    language: Optional[str]
    scrap_series: str
    queue_name: str
    type: ScrapType

    def __init__(
            self,
            task_id: str,
            phrase: str,
            since: datetime.datetime,
            until: datetime.datetime,
            language: Optional[str],
            scrap_series: str,
            queue_name: str
    ):
        object.__setattr__(self, 'task_id', task_id)
        object.__setattr__(self, 'phrase', phrase)
        object.__setattr__(self, 'since', time_utils.remove_microseconds_from_datetime(since))
        object.__setattr__(self, 'until', time_utils.remove_microseconds_from_datetime(until))
        object.__setattr__(self, 'type', ScrapType.SEARCH_BY_PHRASE)
        object.__setattr__(self, 'scrap_series', scrap_series)
        object.__setattr__(self, 'language', language)
        object.__setattr__(self, 'queue_name', queue_name)
        return

    def get_time_interval(self):
        return TimeInterval(self.since, self.until)

    @staticmethod
    def from_dict(dictionary):
        return PhraseScrapTaskParams(
            dictionary['task_id'],
            dictionary['phrase'],
            date_parser(dictionary['since']),
            date_parser(dictionary['until']),
            dictionary['language'],
            dictionary['scrap_series'],
            dictionary['queue_name']
        )
