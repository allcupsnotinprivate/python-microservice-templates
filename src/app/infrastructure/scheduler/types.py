from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TriggerType(str, Enum):
    INTERVAL = "interval"
    CRON = "cron"
    DATE = "date"


@dataclass
class IntervalArgs:
    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    days: int = 0
    weeks: int = 0


@dataclass
class CronArgs:
    year: str | None = None
    month: str | None = None
    day: str | None = None
    week: str | None = None
    day_of_week: str | None = None
    hour: str | None = None
    minute: str | None = None
    second: str | None = None


@dataclass
class DateArgs:
    run_date: datetime | None = None


@dataclass
class JobSchedule:
    trigger_type: TriggerType
    trigger_args: IntervalArgs | CronArgs | DateArgs
    start_time: datetime | None = None
