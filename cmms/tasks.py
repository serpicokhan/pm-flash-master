# Create your tasks here

from celery import shared_task
from cmms.models import *


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)



@shared_task
def send_email_report():
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # wos=schedule.objects.all()
    # print(wos.schNextWo)
    # print(wos.schnextTime)
