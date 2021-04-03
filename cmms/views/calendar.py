'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(nemaintenanceTypebject.OrderId.id)
 '''
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum
import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings

from cmms.models.workorder import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import MaintenanceTypeForm
from django.urls import reverse_lazy
from django.db import transaction
from cmms.models import *
from django.forms.models import model_to_dict
from django.core import serializers
from cmms.business.DateJob import *



def list_calendar(request):
    userg=UserGroup.objects.all()
    maintenanceType=MaintenanceType.objects.all()
    #
    # books = MaintenanceType.objects.all()
    return render(request, 'cmms/calendar/calendar.html', {'ug':userg,'mt':maintenanceType})
def display_calendar(request,mtId,gId,startHijri,endHijri):
    data=dict()
    start,end=DateJob.convert2Date(startHijri,endHijri)
    wo=WorkOrder.objects.none()
    if(mtId=='-1'):

        wo=WorkOrder.objects.filter(visibile=True,isScheduling=False,datecreated__range=(start,end))
    else:
        wo=WorkOrder.objects.filter(maintenanceType=mtId,visibile=True,isScheduling=False,datecreated__range=(start,end))
    if(gId=='-1'):
        pass
    else:
        wo=wo.filter(assignedToUser__in=UserGroups.objects.filter(groupUserGroups=gId).values_list('userUserGroups', flat=True))
        #.values_list('id', 'summaryofIssue','assignedToUser','datecreated','timecreated','dateCompleted','timeCompleted')


    events=[]
    m=MaintenanceType.objects.all()
    mdic={}
    for i in m:
        mdic[i.id]=i.color
    for i in wo:
        color=mdic[i.maintenanceType.id]
        events.append({
        'id':i.id,
        'title':i.summaryofIssue,
        'datecreated':i.datecreated,
        'timecreated':i.timecreated,
        'dateCompleted':i.dateCompleted,
        'timeCompeleted':i.timeCompleted,
        'color':'#FF0000' if i.isEM else color,
        })
    return JsonResponse(events,safe=False)
