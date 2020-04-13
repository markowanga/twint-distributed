import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class TimeInterval:
    since: datetime.datetime
    until: datetime.datetime

    def __init__(self, since: datetime.datetime, until: datetime.datetime):
        object.__setattr__(self, 'since', since)
        object.__setattr__(self, 'until', until)
        return
