from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from logging import getLogger

from cmms.task import demo_task
logger = getLogger(__name__)
@csrf_exempt
def tasks(request,message):
    if request.method == 'GET':
        print("312312")
        return _post_tasks(request,message)

    else:
        return JsonResponse({}, status=405)

def _post_tasks(request,msg):
    message = msg
    print("dsadsa")
    logger.debug('calling demo_task. message={0}'.format(message))
    demo_task(message)
    return JsonResponse({}, status=302)
