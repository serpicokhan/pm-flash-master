'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(neeventbject.OrderId.id)
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
from cmms.tasks.test import *

from cmms.models.event import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import EventForm
from django.urls import reverse_lazy
from django.db import transaction



def list_event(request,id=None):
    #
    books = Events.objects.all()
    return render(request, 'cmms/event/eventList.html', {'event': books,'section':'list_event'})


##########################################################

def save_event_form(request, form, template_name,id=None):


    data = dict()
    if (request.method == 'POST'):
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Events.objects.all()
            data['html_event_list'] = render_to_string('cmms/event/partialEventlist.html', {
                'event': books
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form,'lId':id}


    data['html_event_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
##########################################################


def event_delete(request, id):
    comp1 = get_object_or_404(Event, id=id)
    data = dict()
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies =  Events.objects.all()
        #Tasks.objects.filter(eventId=id).update(event=id)
        data['html_event_list'] = render_to_string('cmms/event/partialEventlist.html', {
            'event': companies
        })
    else:
        context = {'event': comp1}
        data['html_event_form'] = render_to_string('cmms/event/partialEventDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

##########################################################

##########################################################
def event_create(request):
    if (request.method == 'POST'):
        form = EventForm(request.POST)

        return save_event_form(request, form, 'cmms/event/partialEventCreate.html')

    else:

        form = EventForm()
        return save_event_form(request, form, 'cmms/event/partialEventCreate.html')




##########################################################
def event_update(request, id):
    company= get_object_or_404(Event, id=id)
    template=""
    if (request.method == 'POST'):
        form = EventForm(request.POST, instance=company)
    else:
        form = EventForm(instance=company)


    return save_event_form(request, form,"cmms/event/partialEventUpdate.html",id)
##########################################################

##########################################################
