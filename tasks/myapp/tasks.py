from celery import Celery

app = Celery('myapp', broker='redis://localhost:6379/0')


@app.task
def my_periodic_task():
    print('Periodic task executed!')
