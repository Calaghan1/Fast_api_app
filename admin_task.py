import asyncio
from datetime import timedelta

from celery import Celery

from pars_xls import task

celery_app = Celery('admin_task')

celery_app.conf.update(
    broker_url='pyamqp://guest:guest@rabbitmq:5672//',
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Moscow',
    enable_utc=True,
    beat_schedule={
        'main': {
            'task': 'admin_task.main',
            'schedule': timedelta(seconds=15),
        },
    }
)


@celery_app.task
def main() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(task())
