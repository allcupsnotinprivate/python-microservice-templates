import abc
from typing import Any, Callable, cast

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.infrastructure.aClasses import AInfrastructure

from ...utils.tokens import generate_prefixed_uuid
from .logs import wrap_with_log_context
from .types import CronArgs, DateArgs, IntervalArgs, JobSchedule, TriggerType


class ASchedulerManager(AInfrastructure, abc.ABC):
    @abc.abstractmethod
    def start(self, paused: bool) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def shutdown(self, wait: bool) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_job(
        self,
        func: Callable[..., Any],
        schedule: JobSchedule,
        *,
        job_id: str | None = None,
        name: str | None = None,
        args: list[Any] | None = None,
        kwargs: dict[str, Any] | None = None,
        replace_existing: bool = False,
    ) -> None:
        raise NotImplementedError

    def register(
        self,
        schedule: JobSchedule,
        *,
        job_id: str | None = None,
        name: str | None = None,
        args: list[Any] | None = None,
        kwargs: dict[str, Any] | None = None,
        replace_existing: bool = False,
    ) -> Callable[[Callable[..., Any]], Callable[[], None]]:
        def decorator(func: Callable[..., Any]) -> Callable[[], None]:
            def wrapper() -> None:
                self.add_job(
                    func,
                    schedule,
                    job_id=job_id,
                    name=name,
                    args=args,
                    kwargs=kwargs,
                    replace_existing=replace_existing,
                )

            return wrapper

        return decorator


class SchedulerManager(ASchedulerManager):
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()

    def start(self, paused: bool) -> None:
        self.scheduler.start(paused)

    def shutdown(self, wait: bool) -> None:
        self.scheduler.shutdown(wait)

    def add_job(
        self,
        func: Callable[..., Any],
        schedule: JobSchedule,
        *,
        job_id: str | None = None,
        name: str | None = None,
        args: list[Any] | None = None,
        kwargs: dict[str, Any] | None = None,
        replace_existing: bool = False,
    ) -> None:
        trigger = self._build_trigger(schedule)
        job_id = job_id or generate_prefixed_uuid("job", length=16)
        wrapped_func = wrap_with_log_context(job_id=job_id, job_name=name)(func)
        self.scheduler.add_job(
            func=wrapped_func,
            trigger=trigger,
            args=args,
            kwargs=kwargs,
            id=job_id,
            name=name,
            replace_existing=replace_existing,
        )

    @staticmethod
    def _build_trigger(schedule: JobSchedule) -> IntervalTrigger | CronTrigger | DateTrigger:
        match schedule.trigger_type:  # noqa
            case TriggerType.INTERVAL:
                interval_args = cast(IntervalArgs, schedule.trigger_args)
                return IntervalTrigger(**vars(interval_args), start_date=schedule.start_time)
            case TriggerType.CRON:
                cron_args = cast(CronArgs, schedule.trigger_args)
                return CronTrigger(**vars(cron_args), start_date=schedule.start_time)
            case TriggerType.DATE:
                date_args = cast(DateArgs, schedule.trigger_args)
                run_date = date_args.run_date or schedule.start_time
                return DateTrigger(run_date=run_date)
            case _:
                raise NotImplementedError(f"Unsupported trigger type: {schedule.trigger_type}")
