from celery import Celery

app = Celery('myapp', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'my-periodic-task': {
        'task': 'myapp.tasks.my_periodic_task',  # Путь к вашей задаче
        'schedule': 10.0  # Интервал выполнения в секундах
    },
}

app.conf.timezone = 'UTC'