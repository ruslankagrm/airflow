from time import sleep

from celery import group, Celery
from celery.result import AsyncResult
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from FlightSearchManager import FlightSearchManager
from Pricer import Pricer
from models import SearchTaskResult
from redis_client import RedisClient, REDIS_HOST, REDIS_PORT

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0', backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
celery_log = get_task_logger(__name__)

celery.conf.beat_schedule = {
    'update_rates_for_price': {
        'task': 'update_rates',
        'schedule': crontab(hour=12)
    },
}


def get_tasks_result(search_id: str) -> SearchTaskResult:
    tasks_result = AsyncResult(search_id)
    search_result = SearchTaskResult(**{"search_id": search_id,
                                        "status": "str",
                                        "items": []})
    if tasks_result.children and tasks_result.children[0].children:
        first_provider_task = tasks_result.children[0].children[0]
        second_provider_task = tasks_result.children[0].children[1]
        search_result.status = tasks_result.children[0].children[0].status
        if tasks_result.children[0].ready():
            search_result.items = first_provider_task.result + second_provider_task.result
    return search_result


@celery.task(name="call_first_provider")
def call_first_provider() -> dict:
    sleep(30)
    file_path = 'response_a.json'
    return FlightSearchManager(file_path).search_flights()


@celery.task(name="call_second_provider")
def call_second_provider() -> dict:
    sleep(60)
    file_path = 'response_b.json'
    return FlightSearchManager(file_path).search_flights()


@celery.task(name="create_search_tasks")
def create_search_tasks():
    task_group = group([call_first_provider.s(), call_second_provider.s()])
    return task_group()


@celery.task(name="update_rates")
def update_rates():
    pricer = Pricer()
    rates = pricer.update_rates()
    RedisClient().set(key=pricer.redis_key, value=str(rates))
    return rates
