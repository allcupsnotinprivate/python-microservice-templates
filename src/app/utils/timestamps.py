from datetime import datetime, timedelta

from pytz import utc


def now_with_tz(delta: timedelta | None = None) -> datetime:
    now = datetime.now(utc)
    if delta:
        now += delta
    return now
