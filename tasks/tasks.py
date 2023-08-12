from celery import Celery
from time import sleep
from pars_xls import check_xlsx
celery = Celery('tasks',  broker='redis://localhost:6379')


@celery.task
async def check():
    check_xlsx()

# @celery_app.task
# def reverse(text):
#     sleep(5)
#     return text    