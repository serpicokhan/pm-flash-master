'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(newobject.OrderId.id)
 '''
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings
from cmms.models.workorder import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#from django.core import serializers
import json
from django.forms.models import model_to_dict
from cmms.forms import WoMiscForm
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper

def filterUser(request,books):
    if(request.user.username!="admin"):
        books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated')
    return books

###################################################################



def list_woMisc(request,id=None):
    books = MiscCost.objects.all()
    return render(request, 'cmms/workorder_misccoast/woMiscList.html', {'woMiscs': books})


###################################################################
@permission_required('cmms.view_misccost')
def js_list_woMisc(request,woId):
    data=dict()
    books=MiscCost.objects.filter(miscCoastWorkorder=woId)

    data['html_woMisc_list']= render_to_string('cmms/workorder_misccoast/partialWoMiscList.html', {
        'woMiscs': books,
        'perms': PermWrapper(request.user)
    })
    data['form_is_valid']=True
    return JsonResponse(data)


###################################################################    ###################################################################
@csrf_exempt
def save_woMisc_form(request, form, template_name,woId=None):
    data = dict()
    if (request.method == 'POST'):
          if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fmt = getattr(settings, 'LOG_FORMAT', None)
            lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
            logging.basicConfig(format=fmt, level=lvl)
            logging.debug( woId)
            books = MiscCost.objects.filter(miscCoastWorkorder=woId)
            data['html_woMisc_list'] = render_to_string('cmms/workorder_misccoast/partialWoMiscList.html', {
                'woMiscs': books,
                'perms': PermWrapper(request.user)
            })
          else:
              fmt = getattr(settings, 'LOG_FORMAT', None)
              lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
              logging.basicConfig(format=fmt, level=lvl)
              logging.debug( form.errors)

    context = {'form': form}
    data['html_woMisc_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
###################################################################

@csrf_exempt
def woMisc_delete(request, id):
    comp1 = get_object_or_404(MiscCost, id=id)
    data = dict()
    woId=comp1.miscCoastWorkorder
    if (request.method == 'POST'):
        comp1.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        companies = MiscCost.objects.filter(miscCoastWorkorder=woId)
        data['html_woMisc_list'] = render_to_string('cmms/workorder_misccoast/partialWoMiscList.html', {
            'woMiscs': companies
        })
    else:
        context = {'woMisc': comp1}
        data['html_woMisc_form'] = render_to_string('cmms/workorder_misccoast/partialWoMiscDelete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
###################################################################
@csrf_exempt
def woMisc_create(request):
    woId=-1
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
    logging.basicConfig(format=fmt, level=lvl)
    logging.debug( "dasdsadasdsa")
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)


        data = request.POST.dict()
        print("#######################")
        print(body)

        data['miscCoastWorkorder']=body['miscCoastWorkorder']
        data['miscCoastType']=body['miscCoastType']
        data['miscCoastdescription']=body['miscCoastdescription']
        data['estimatedQnty']=body['estimatedQnty']
        data['estimatedUnitCoast']=body['estimatedUnitCoast']
        data['estimatedTotalCoast']=body['estimatedTotalCoast']
        data['qnty']=body['qnty']
        data['actualUnitCoast']=body['actualUnitCoast']
        data['actualTotlaCoast']=body['actualTotlaCoast']
        data['miscCoastIndividual']=body['miscCoastIndividual']
        woId=body['miscCoastWorkorder']


        form = WoMiscForm(data)

    else:
        form = WoMiscForm()
    return save_woMisc_form(request, form, 'cmms/workorder_misccoast/partialWoMiscCreate.html',woId)
###################################################################

@csrf_exempt
def woMisc_update(request, id):
    company= get_object_or_404(MiscCost, id=id)
    woId=company.miscCoastWorkorder
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = request.POST.dict()

        data['miscCoastWorkorder']=body['miscCoastWorkorder']
        data['miscCoastType']=body['miscCoastType']
        data['miscCoastdescription']=body['miscCoastdescription']
        data['estimatedQnty']=body['estimatedQnty']
        data['estimatedUnitCoast']=body['estimatedUnitCoast']
        data['estimatedTotalCoast']=body['estimatedTotalCoast']
        data['qnty']=body['qnty']
        data['actualUnitCoast']=body['actualUnitCoast']
        data['actualTotlaCoast']=body['actualTotlaCoast']
        data['miscCoastIndividual']=body['miscCoastIndividual']
        form = WoMiscForm(data, instance=company)
    else:
        form = WoMiscForm(instance=company)
    return save_woMisc_form(request, form, 'cmms/workorder_misccoast/partialWoMiscUpdate.html',woId)
