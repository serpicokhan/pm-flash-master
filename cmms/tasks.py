from celery import task
from celery import shared_task
# We can have either registered task
@task(name='summary')
def send_import_summary():
     print("321321")
# or
@shared_task
def send_notifiction():
     print("dsdsdsa")
     # Another trick
