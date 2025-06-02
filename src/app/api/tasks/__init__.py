from app.infrastructure import ASchedulerManager, IntervalArgs, JobSchedule, TriggerType

from .stats import get_conversations_stats


def register_tasks(scheduler_manager: ASchedulerManager) -> None:
    scheduler_manager.add_job(
        get_conversations_stats,
        JobSchedule(trigger_type=TriggerType.INTERVAL, trigger_args=IntervalArgs(seconds=10)),
        job_id="get_conversations_stats",
        name="Conversations Statistics",
        replace_existing=True,
    )


__all__ = ["register_tasks"]
