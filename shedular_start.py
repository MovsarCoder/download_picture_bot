from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from database.crud_sqlalchemy import decrement_vip_panel_days, delete_user_vip_panel_where_less_then_0_days


def start_scheduler():
    scheduler = AsyncIOScheduler(timezone=timezone("Europe/Moscow"))

    # Каждый день в 10:00 по Москве
    scheduler.add_job(decrement_vip_panel_days, CronTrigger(hour=10, minute=0))
    scheduler.add_job(delete_user_vip_panel_where_less_then_0_days, CronTrigger(hour=10, minute=0))

    # Каждые 10 секунд
    # from apscheduler.triggers.interval import IntervalTrigger
    # scheduler.add_job(
    #     decrement_vip_panel_days,
    #     IntervalTrigger(seconds=10)  # Каждый день в 10:00 по Москве
    # )

    scheduler.start()
    print("Шедулер запущен.")
