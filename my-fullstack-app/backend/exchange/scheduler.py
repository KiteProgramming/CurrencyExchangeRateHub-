from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from .tasks import fetch_exchange_rates
import logging

logger = logging.getLogger('django')

def scheduled_job():
    logger.debug("Running scheduled job: fetch_exchange_rates")
    fetch_exchange_rates(api_choice='XE')

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        scheduled_job,
        trigger='interval',
        minutes=60,
        id='fetch_exchange_rates_job',
        replace_existing=True
    )

    register_events(scheduler)
    scheduler.start()
    logger.debug("Scheduler started")

    scheduled_job()