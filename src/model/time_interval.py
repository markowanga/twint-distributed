import datetime


class TimeInterval:
    def __init__(self, start: datetime.datetime, end: datetime.datetime):
        self._start = start
        self._end = end

    def get_start(self) -> datetime.datetime:
        return self._start

    def get_end(self) -> datetime.datetime:
        return self._end

    def __repr__(self):
        return "TimeInterval(start=" + str(self._start) + ", end=" + str(self._end) + ")"
