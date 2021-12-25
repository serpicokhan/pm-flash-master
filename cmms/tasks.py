# Create your tasks here

from celery import shared_task
from cmms.models import *
from django.contrib.admin.models import LogEntry, ADDITION,CHANGE,DELETION


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
    wos=Schedule.objects.all()
    print(wos.schNextWo)
    print(wos.schnextTime)
    LogEntry.objects.log_action(
        user_id         = 1,
        content_type_id = 1,
        object_id       = 1,
        object_repr     = 'celery',
        action_flag     = ADDITION,
        change_message= '1221'
    )
