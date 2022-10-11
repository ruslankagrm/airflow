import asyncio
import os
from time import sleep

from celery import Celery
from celery.utils.log import get_task_logger

from FlightSearchManager import FlightSearchManager

celery = Celery('tasks', broker='redis://localhost:6379')
# Create logger - enable to display messages on task logger
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
celery_log = get_task_logger(__name__)


async def call_first_provider():
    await asyncio.sleep(30)
    file_path = 'response_a.json'
    return await FlightSearchManager(file_path).search_flights()


async def call_second_provider():
    await asyncio.sleep(30)
    file_path = 'response_b.json'
    return await FlightSearchManager(file_path).search_flights()


@celery.task(name="create_task")
def create_task():
    # first = await call_first_provider()
    # second = await call_second_provider()
    # first.append(second)
    sleep(5)
    return "first"

